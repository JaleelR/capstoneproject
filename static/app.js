
/////////////Adds post functions/////////////


function addOnsubmit() {
    $("#success").on("click", function (e) {
        e.preventDefault();
        let textform = $("#inputpost");
        let userId = $("h1").data("user");
        let postText = textform.val();
        if (postText.trim() === "") {
            $("#error-message").text("Dude! motivate us. We can't get something from nothing!");
            return;
        }
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
               
                
                let post = `<div class="articles"><li class="article item" id="${response.id}" data-id="${response.id}" data-user="${userId}"><div class="post-content">  <div class="user-info">  <img class ="img-container" src="${response.img}" > <b>${response.username}</b> </div>  ${document.createTextNode(postText).textContent}
                 <form id="delete-form" action="/post/${response.id}/delete" method="post"><button class="remove"  id="danger" data-post="${response.id}">Delete</button> </form></div> 
                </li></div></div>`;
                $(".postsection").prepend(post);
                const flashMessagesDiv = document.getElementById("flash-messages");

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



/////////////Delete post functions/////////////
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
    



/////////////functions to show youtube videos/////////////

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





/////////////Adding videos to server/////////////
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


 


   









