document.addEventListener("DOMContentLoaded", () => {
    const postButton = document.getElementById("postButton");
    const postModal = document.getElementById("postModal");
    const closeModal = document.querySelector(".close-btn");
    const submitPost = document.getElementById("submitPost");

    postButton.addEventListener("click", () => {
        postModal.style.display = "flex";
    });

    closeModal.addEventListener("click", () => {
        postModal.style.display = "none";
    });

    submitPost.addEventListener("click", async () => {
        const postContent = document.getElementById("postContent").value;
        const userId = 1;

        if (postContent.trim() !== "") {
            const response = await fetch('/messages', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    user_id: userId,
                    message_content: postContent
                })
            });

            if (response.ok) {
                alert("Your post has been submitted!");
                postModal.style.display = "none";
                document.getElementById("postContent").value = "";
            } else {
                alert("Error submitting your post.");
            }
        } else {
            alert("Post cannot be empty!");
        }
    });
});

async function likeMessage(messageId) {
    const response = await fetch(`/messages/${messageId}/like`, {
        method: 'POST'
    });

    if (response.ok) {
        alert('Message liked!');
    } else {
        alert('Error liking the message.');
    }
}
