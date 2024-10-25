document.addEventListener("DOMContentLoaded", () => {
    const sidebarLinks = document.querySelectorAll(".sidebar ul li a");
    const feedItems = document.querySelectorAll(".feed-item");
    const toggleBtn = document.getElementById("toggle-sidebar");
    const sidebar = document.querySelector(".sidebar");

    // Toggle sidebar NOT WORKING CURRENTLY
    if (toggleBtn) {
        toggleBtn.addEventListener("click", () => {
            sidebar.classList.toggle("open");
        });
    }

    // Sidebar link hover animations
    sidebarLinks.forEach(link => {
        link.addEventListener("mouseover", () => {
            link.style.transition = "color 0.3s ease, padding-left 0.3s ease";
            link.style.paddingLeft = "1.5rem"; 
            link.style.color = "#ffffff"; 
        });
        link.addEventListener("mouseout", () => {
            link.style.paddingLeft = "1rem"; 
            link.style.color = "#e0e0e0"; 
        });
    });

    // Scroll animation to fade in feed items when they come into view
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = 1;
                entry.target.style.transform = "translateY(0)";
                observer.unobserve(entry.target); 
            }
        });
    }, { threshold: 0.2 });

    feedItems.forEach(item => {
        item.style.opacity = 0;  
        item.style.transform = "translateY(30px)"; 
        observer.observe(item);  
    });
});
