document.addEventListener("DOMContentLoaded", function () {
    // Sélectionne le bouton et le compteur de likes
    let likeBtn = document.getElementById("likeButton");
    let likeCount = document.getElementById("likes");

    likeBtn.addEventListener("click", function () {
        // Envoie une requête POST au serveur flask.
        let idAmateur = "user_id_example"; // l'ID réel de l'utilisateur connecté remplace l'IdAm
        
        fetch(window.location.origin + "/like/" + likeBtn.dataset.id, {
            method: "POST",
            body: new URLSearchParams({
                "IdAm": idAmateur  // Ajoute l'Id de l'amateur dans la requête
            })
        })
        .then(response => response.json()) // Convertit la réponse en JSON
        .then(data => {
            likeCount.textContent = data.likes; // Met à jour le compteur
            let historique = document.getElementById("historiqueLikes");
            historique.innerHTML = "";  // Vide l'historique actuel
            data.utilisateurs_likes.forEach(function(utilisateur) {
                let li = document.createElement("li");
                li.textContent = utilisateur;
                historique.appendChild(li);
            });
        })
        .catch(error => console.error("Erreur :", error)); // Gère les erreurs
    });
});
