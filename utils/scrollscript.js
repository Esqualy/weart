// Cléménce Chateau
document.addEventListener("DOMContentLoaded", function () {
    let gallery = document.getElementById("gallery");

    let images = [
        "https://source.unsplash.com/200x200/?painting",
        "https://source.unsplash.com/200x200/?art",
        "https://source.unsplash.com/200x200/?abstract",
        "https://source.unsplash.com/200x200/?sculpture",
        "https://source.unsplash.com/200x200/?streetart",
        "https://source.unsplash.com/200x200/?modernart"
    ];

    images.forEach(src => {
        let img = document.createElement("img");
        img.src = src;
        gallery.appendChild(img);
    });

    // Défilement automatique (comme TikTok/Instagram)
    function autoScroll() {
        gallery.scrollBy({ left: 110, behavior: "smooth" });

        // Si on arrive à la fin, revenir au début
        if (gallery.scrollLeft + gallery.clientWidth >= gallery.scrollWidth) {
            gallery.scrollTo({ left: 0, behavior: "smooth" });
        }
    }

    setInterval(autoScroll, 2000); // Défilement toutes les 2 secondes
});
