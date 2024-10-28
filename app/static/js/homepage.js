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
    }
    else {
        const response_data = await response.json();
        if (response_data.message == "Already liked this post")
            {
            alert("You have already liked this message!")
            }
        else{
        alert('Error liking the message.');
        }
    }
}

document.getElementById("logout").addEventListener("click", function() {
    window.location.href = "/logout";
});

async function loadPosts()
{
    const response = await fetch('/api/posts');
    const post_data = await response.json();
    const content = document.getElementById('content');

    post_data.posts.forEach(post => {
    //Added each post to the html in the format
//    <section class="feed-item">
//                <img src="../static/images/workout1.jpg" alt="Workout Example 1">
//                <p>Push yourself to the limit! 💪 #Strength</p>
//    </section>
    const section = document.createElement('section');
    section.classList.add('feed-item');


    const messageContent  = document.createElement('p');
    messageContent.textContent = post.message_content;
    const username = document.createElement('p');
        username.textContent = `Posted by: ${post.username}`;
    const likes = document.createElement('p');
        likes.textContent = `Likes: ${post.likes}`;
    const timestamp = document.createElement('time');
        timestamp.textContent = `Posted on: ${post.created_at}`;
    const likebutton =  document.createElement('like-button');
    likebutton.classList.add('like-button');
    likebutton.textContent ="Like!"
    likebutton.addEventListener('click', async () => {
        const response = await likeMessage(post.message_id);
        if (response.ok) {
                likes.textContent = `Likes: ${post.likes + 1}`;
            }
    });
        section.appendChild(messageContent);
        section.appendChild(username);
        section.appendChild(likes);
        section.appendChild(timestamp);
        section.appendChild(likebutton);
    content.insertBefore(section, content.firstChild);
    });


}

window.onload = function() {
    loadPosts();
};
