function addOnsubmit() {
    $("#success").on("click", function (e) {
        e.preventDefault();
        let textform = $("#inputpost");
        let userId = $("h1").data("user");
        let postText = textform.val();
        addPost(userId, postText);
        textform.val("")
    });
}

addOnsubmit();

function addPost(userId, postText) {
    let textform = $("#text");

    try {
        $.ajax({
            url: `/home/${userId}`,
            data: JSON.stringify({
                "text": postText,
                "user_id": userId,

            }),
            dataType: "json",
            contentType: "application/json",
            method: "POST",

            success: function (response) {

                console.log(postText, userId)
                console.log(response);
                let img = response.img
                let post = `<div class="articles"><li class="article item" id="${response.id}" data-id="${response.id}" data-user="${userId}"><div class="post-content">   <img class = "img-container" src="${img}"><bid=postname>${response.username}</bid=postname> ${document.createTextNode(postText).textContent}
                 <form id="delete-form" action="/post/${response.id}/delete" method="post"><button class="remove"  id="danger" data-post="${response.id}">Delete</button> </form></div> 
                </li></div></div>`;
                $(".postsection").prepend(post);
                
                $("#delete-form").on("submit", function(e) {
                    e.preventDefault();
                    const post = $(this).closest("li");
                    deletePostsRequest(post, response.id )

                })
            
            },
            error: function (xhr, status, error) {
                console.error("AJAX Error:", error);
            }
        });
    } catch (error) {
        console.error("An error occurred while attempting to create post", error);
    }
}




function deletePostsOnSubmit() {
    $(".remove").on("click", function (e) {
        e.preventDefault();
        const post = $(this).closest("li");
        const postId = post.data("id")
        deletePostsRequest(post, postId)
    })
}


function deletePostsRequest(post, postId) {
    try {
        $.ajax({
            url: `/post/${postId}/delete`,
            method: 'POST',
            success: function (response) {
                console.log(response.message)
                post.remove()

            }
        })

    }
    catch (error) {
        console.error('Error deleting post:', error);
    }
}

deletePostsOnSubmit()


let userId = $("h1").data("user")

function addVideosOnClick() { 
    $(".see-more-vids").on("click", function (e) {
        e.preventDefault();
        addVideosFromServer()
       
    })
}
    




function embeddedYoutubePosts() {
    try {
        $(".vidsection li").each(function (index) {
            let listItem = $(this);

            const vidid = listItem.data("vidid")

            const embedUrl = `https://www.youtube.com/embed/${vidid}`
            const frame = $("<iframe>")
            frame.attr("src", embedUrl);
            frame.width = 560;
            frame.height = 315;
            frame.allowFullscreen = true;
            listItem.append(frame)
        }
        )
    }
    catch (error) {
        console.error("An error has occured in YoutubeEmbeddedPosts", error)
    }
}
embeddedYoutubePosts();






function addVideosFromServer() {
    let pageCount = 1;
    $.ajax({
        url: `/home/${userId}`,
        method: "GET",
        dataType: "json",
        
        success: function (response) {
          
  
                 
  
        },
            complete: function () {
                isLoading = false;
            },
            error: function (error) {
                console.error("Errrorrrrrr", error)
            }
        })

     }
addVideosOnClick()










