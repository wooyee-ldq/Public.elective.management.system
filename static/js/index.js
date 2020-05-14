$(document).ready(function(){

    // 退出按钮点击事件
    $("#quit").click(function(){
        $("#exit").slideToggle(500);
    })


    // 全局的按键按下后升起的事件：
    $(document).keyup(function (e) {
        // Esc事件：
        if (e.keyCode == 27) {
            $('#exit').slideToggle(500);
        }

    });

    // 退出取消按钮点击事件
    $("#cancel_exit").click(function(){
        $("#exit").slideToggle(500);
    })

    //  // 关闭浏览器事件
    //  $(window).bind('beforeunload',function(){
    //     alert("确认要离开此页面吗？")
    //     let bl = confirm("确认要离开此页面吗？")
    //     if(bl){
    //         $.get($("#exit a").attr("href"))
    //     }
    // })

})
