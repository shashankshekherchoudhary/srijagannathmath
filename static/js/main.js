document.addEventListener('DOMContentLoaded', function() {
    // 1. Gallery Lightbox Modal
    // When modal opens, update image src, title, and description from data attributes
    const galleryModal = document.getElementById('galleryModal');
    if (galleryModal) {
        galleryModal.addEventListener('show.bs.modal', function(event) {
            const trigger = event.relatedTarget;
            const imgSrc = trigger.getAttribute('data-img-src');
            const imgTitle = trigger.getAttribute('data-img-title');
            const imgDesc = trigger.getAttribute('data-img-desc');

            const modalImage = document.getElementById('galleryModalImage');
            const modalTitle = document.getElementById('galleryModalTitle');
            const modalDesc = document.getElementById('galleryModalDescription');
            const modalDescContainer = document.getElementById('galleryModalDescriptionContainer');

            if (modalImage) {
                modalImage.src = imgSrc;
                modalImage.alt = imgTitle || 'Gallery Image';
            }
            if (modalTitle) modalTitle.textContent = imgTitle || '';

            // I8: Toggle description container visibility
            if (imgDesc && imgDesc.trim()) {
                if (modalDesc) modalDesc.textContent = imgDesc;
                if (modalDescContainer) modalDescContainer.style.display = 'block';
            } else {
                if (modalDescContainer) modalDescContainer.style.display = 'none';
            }
        });
    }

    // 2. Copy to Clipboard
    document.querySelectorAll('.btn-copy').forEach(function(btn) {
        btn.addEventListener('click', function() {
            const text = this.getAttribute('data-copy-text');
            const button = this;

            if (navigator.clipboard && window.isSecureContext) {
                navigator.clipboard.writeText(text).then(function() {
                    showCopyFeedback(button);
                    showCopyToast('Copied successfully! ✓');
                }).catch(function() {
                    fallbackCopyTextToClipboard(text, button);
                });
            } else {
                fallbackCopyTextToClipboard(text, button);
            }
        });
    });

    function fallbackCopyTextToClipboard(text, button) {
        const textarea = document.createElement('textarea');
        textarea.value = text;
        textarea.style.position = 'fixed';
        textarea.style.opacity = '0';
        document.body.appendChild(textarea);
        textarea.focus();
        textarea.select();
        try {
            document.execCommand('copy');
            showCopyFeedback(button);
            showCopyToast('Copied successfully! ✓');
        } catch (err) {
            console.error('Fallback: Unable to copy', err);
            showCopyToast('Failed to copy. Please try manually.');
        }
        document.body.removeChild(textarea);
    }

    // Visual feedback on the copy button itself
    function showCopyFeedback(button) {
        const icon = button.querySelector('i');
        if (icon) {
            const originalClass = icon.className;
            icon.className = 'bi bi-check2 text-success';
            setTimeout(function() {
                icon.className = originalClass;
            }, 2000);
        }
    }

    // 3. Copy Toast
    function showCopyToast(message) {
        // Remove existing toast if any
        const existing = document.querySelector('.copy-toast');
        if (existing) existing.remove();

        const toast = document.createElement('div');
        toast.className = 'copy-toast';
        toast.setAttribute('role', 'status');
        toast.setAttribute('aria-live', 'polite');
        toast.textContent = message;
        document.body.appendChild(toast);

        // Trigger animation
        setTimeout(function() { toast.classList.add('show'); }, 10);

        // Remove after 2 seconds
        setTimeout(function() {
            toast.classList.remove('show');
            setTimeout(function() { toast.remove(); }, 300);
        }, 2000);
    }

    // 4. Smooth Scroll for anchor links (M7: wrapped in try-catch)
    document.querySelectorAll('a[href^="#"]').forEach(function(anchor) {
        anchor.addEventListener('click', function(e) {
            const href = this.getAttribute('href');
            if (href && href !== '#') {
                try {
                    const target = document.querySelector(href);
                    if (target) {
                        e.preventDefault();
                        target.scrollIntoView({ behavior: 'smooth', block: 'start' });
                    }
                } catch (err) {
                    // Invalid selector — ignore silently
                }
            }
        });
    });

    // 5. Close mobile nav on link click
    const navLinks = document.querySelectorAll('.navbar-nav .nav-link');
    const navCollapse = document.querySelector('.navbar-collapse');
    navLinks.forEach(function(link) {
        link.addEventListener('click', function() {
            if (navCollapse && navCollapse.classList.contains('show')) {
                if (typeof bootstrap !== 'undefined') {
                    const bsCollapse = bootstrap.Collapse.getInstance(navCollapse);
                    if (bsCollapse) bsCollapse.hide();
                } else {
                    navCollapse.classList.remove('show');
                }
            }
        });
    });

    // 6. Scroll-based navbar shadow
    const navbar = document.querySelector('.navbar-temple');
    if (navbar) {
        window.addEventListener('scroll', function() {
            if (window.scrollY > 50) {
                navbar.classList.add('navbar-scrolled');
            } else {
                navbar.classList.remove('navbar-scrolled');
            }
        });
    }
});
