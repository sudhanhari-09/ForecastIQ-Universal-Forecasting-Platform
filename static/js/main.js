document.addEventListener('DOMContentLoaded', function () {
    /* ===== Auto-dismiss Alerts ===== */
    var alerts = document.querySelectorAll('.alert-dismissible');
    alerts.forEach(function (alert) {
        setTimeout(function () {
            var bsAlert = bootstrap.Alert.getOrCreateInstance(alert);
            if (bsAlert) bsAlert.close();
        }, 6000);
    });

    /* ===== Sidebar Active Link ===== */
    var currentPath = window.location.pathname;
    document.querySelectorAll('.sidebar-nav a').forEach(function (link) {
        var href = link.getAttribute('href');
        if (href && href !== '#' && currentPath === href) {
            link.classList.add('active');
        }
    });

    var sidebar = document.getElementById('appSidebar');
    if (sidebar) {
        sidebar.querySelectorAll('.sidebar-nav a').forEach(function (link) {
            var href = link.getAttribute('href');
            if (href && href !== '#' && currentPath.startsWith(href) && href !== '/') {
                link.classList.add('active');
            }
        });
    }

    /* ===== Sidebar Toggle ===== */
    var sidebarToggle = document.getElementById('sidebarToggle');
    var overlay = document.getElementById('sidebarOverlay');

    if (sidebarToggle && sidebar) {
        sidebarToggle.addEventListener('click', function () {
            sidebar.classList.toggle('show');
            if (overlay) overlay.classList.toggle('show');
        });
    }

    if (overlay) {
        overlay.addEventListener('click', function () {
            sidebar.classList.remove('show');
            overlay.classList.remove('show');
        });
    }

    /* ===== Animated Counters ===== */
    function animateCounter(el) {
        var text = el.textContent.trim();
        var num = parseFloat(text.replace(/[^0-9.-]/g, ''));
        if (isNaN(num)) return;

        var suffix = text.replace(/[0-9.-]/g, '');
        var isInt = Number.isInteger(num);
        var duration = 800;
        var startTime = performance.now();

        function update(currentTime) {
            var elapsed = currentTime - startTime;
            var progress = Math.min(elapsed / duration, 1);
            var eased = 1 - Math.pow(1 - progress, 3);
            var current = eased * num;

            var display = isInt ? Math.round(current) : current.toFixed(1);
            el.textContent = display + suffix;

            if (progress < 1) {
                requestAnimationFrame(update);
            } else {
                el.textContent = text;
            }
        }

        requestAnimationFrame(update);
    }

    /* Animate stat values on first scroll into view */
    var counterObserver = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
            if (entry.isIntersecting) {
                var el = entry.target;
                animateCounter(el);
                counterObserver.unobserve(el);
            }
        });
    }, { threshold: 0.5 });

    document.querySelectorAll('.stat-card-value, .stat-box h3, .stat-box h4, .stat-box .stat-number').forEach(function (el) {
        counterObserver.observe(el);
    });

    /* ===== Card Scroll Animations (Fade + Slide Up) ===== */
    var cardObserver = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
                cardObserver.unobserve(entry.target);
            }
        });
    }, { threshold: 0.1 });

    document.querySelectorAll('.stat-card, .section-card, .quick-action-card, .mode-card').forEach(function (card) {
        card.style.opacity = '0';
        card.style.transform = 'translateY(12px)';
        card.style.transition = 'opacity 0.35s ease-out, transform 0.35s ease-out';
        cardObserver.observe(card);
    });

    /* ===== Upload Zone Enhancements ===== */
    var dropZones = document.querySelectorAll('.upload-zone');
    dropZones.forEach(function (zone) {
        zone.addEventListener('dragover', function (e) {
            e.preventDefault();
            this.classList.add('dragover');
        });

        zone.addEventListener('dragleave', function () {
            this.classList.remove('dragover');
        });

        zone.addEventListener('drop', function () {
            this.classList.remove('dragover');
        });
    });
});