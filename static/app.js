

function appendAndEmptyPost(){
try {
    var textform = $("#text");
    var postContent = $(".postsection li").text();
    textform.val(textform.val() + postContent);
    textform.val("")
    }
    catch(error) {
        console.error("an error had occured in appendEmpty post", error)
    }
}
appendAndEmptyPost()




$(".remove").css("color", "red")




function embeddedYoutubePosts() {
try {
    $(".vidsection li").each(function(index){
        let listItem = $(this);
        const vidid = listItem.data("vidid")
        console.log(vidid)
        const embedUrl = `https://www.youtube.com/embed/${vidid}`
        const frame = $("<iframe>")
        frame.attr("src", embedUrl);
        frame.width = 560;
        frame.height = 315;
        frame.allowFullscreen = true;
        listItem.append(frame)
    }
)}
catch(error){
    console.error("An error has occured in YoutubeEmbeddedPosts", E)
}
}
embeddedYoutubePosts();

















    





