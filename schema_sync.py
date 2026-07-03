import os
from sqlalchemy import types, text


def _get_db_path(app):
    uri = app.config['SQLALCHEMY_DATABASE_URI']
    if uri.startswith('sqlite:///'):
        return uri[len('sqlite:///'):]
    return None


def _sqltype_name(col_type):
    if isinstance(col_type, types.Integer):
        return 'INTEGER'
    if isinstance(col_type, types.Float):
        return 'FLOAT'
    if isinstance(col_type, types.String):
        length = getattr(col_type, 'length', None)
        return 'VARCHAR(%d)' % length if length else 'VARCHAR'
    if isinstance(col_type, types.Text):
        return 'TEXT'
    if isinstance(col_type, types.DateTime):
        return 'DATETIME'
    if isinstance(col_type, types.Boolean):
        return 'BOOLEAN'
    return type(col_type).__name__.upper()


def _get_column_default(col):
    if col.default is None:
        return None
    try:
        raw = col.default.arg if hasattr(col.default, 'arg') else col.default
        if callable(raw):
            return None
        return raw
    except (ValueError, AttributeError):
        return None


def _format_default_sql(raw):
    if raw is None:
        return None
    if isinstance(raw, str):
        return "'%s'" % raw
    if isinstance(raw, bool):
        return '1' if raw else '0'
    return str(raw)


def _get_db_columns(engine, table_name):
    with engine.connect() as conn:
        result = conn.execute(
            text("PRAGMA table_info(%s)" % table_name)
        )
        return {row[1] for row in result}


def _get_table_names(engine):
    with engine.connect() as conn:
        result = conn.execute(
            text("SELECT name FROM sqlite_master WHERE type='table'")
        )
        return {row[0] for row in result}


def sync_schema(app):
    db_path = _get_db_path(app)
    if not db_path:
        return

    db_path = os.path.abspath(db_path)
    if not os.path.exists(db_path):
        return

    from database import db

    if not db.engine:
        return

    engine = db.engine
    tables_in_db = _get_table_names(engine)

    for model in db.Model.__subclasses__():
        table_name = model.__tablename__

        if table_name not in tables_in_db:
            continue

        existing_db_cols = _get_db_columns(engine, table_name)
        model_cols = model.__table__.columns

        missing_cols = [
            col for col in model_cols
            if col.name not in existing_db_cols
        ]

        if not missing_cols:
            continue

        for col in missing_cols:
            col_type_str = _sqltype_name(col.type)
            default_raw = _get_column_default(col)
            default_sql = _format_default_sql(default_raw)

            sql = "ALTER TABLE %s ADD COLUMN %s %s" % (
                table_name, col.name, col_type_str
            )
            if default_sql is not None:
                sql += " DEFAULT %s" % default_sql

            try:
                with engine.connect() as conn:
                    conn.execute(text(sql))
                    conn.commit()

                existing_db_cols.add(col.name)

                if default_sql is not None and not col.nullable:
                    with engine.connect() as conn:
                        conn.execute(text(
                            "UPDATE %s SET %s = %s WHERE %s IS NULL" %
                            (table_name, col.name, default_sql, col.name)
                        ))
                        conn.commit()
            except Exception:
                pass
