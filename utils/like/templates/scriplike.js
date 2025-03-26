document.addEventListener("DOMContentLoaded", function () {
    // Sélectionne le bouton et le compteur de likes
    let likeBtn = document.getElementById("like-btn");
    let likeCount = document.getElementById("like-count");

    likeBtn.addEventListener("click", function () {
        // Envoie une requête POST au serveur Flask
        fetch(window.location.origin + "/like/" + likeBtn.dataset.id, {
            method: "POST"
        })
        .then(response => response.json()) // Convertit la réponse en JSON
        .then(data => {
            likeCount.textContent = data.likes; // Met à jour le compteur
        })
        .catch(error => console.error("Erreur :", error)); // Gère les erreurs
    });
});
