$(document).ready(function () {

    $(".show").hide()
    $("#index").show()

    // 导航栏切换显示
    $("#nav ul").on('click', 'li', function () {
        $(this).siblings("li").removeClass("active")
        $(this).addClass("active")
        $(".show").hide()
        let tip = $(this).attr("tip")
        $("#" + tip).show()
    });


    // 修改密码取消按钮点击事件
    $("#cancel_chpwd").click(function () {
        $("#old_pwd").val("")
        $("#new_pwd1").val("")
        $("#new_pwd2").val("")
    })

    // 修改密码确认按钮点击事件
    $("#sure_chpwd").click(function () {
        let pwd = $("#old_pwd")
        let pwd1 = $("#new_pwd1")
        let pwd2 = $("#new_pwd2")
        let old_pwd = pwd.val()
        let new_pwd1 = pwd1.val()
        let new_pwd2 = pwd2.val()
        if (old_pwd == "" || new_pwd1 == "" || new_pwd2 == "") {
            alert("字段不能为空！")
        } else {
            let bl = confirm("确认修改密码？")
            if (bl == false) {
                return
            }
            pwd.val("")
            pwd1.val("")
            pwd2.val("")
            $.ajax({
                url: "/tea/changePwd",
                method: "post",
                async: true,
                dataType: "json",
                data: {
                    "old_pwd": old_pwd,
                    "new_pwd1": new_pwd1,
                    "new_pwd2": new_pwd2
                },
                success: function (msg) {
                    alert(msg.tip)
                },
                error: function () {
                    alert("修改失败！")
                }
            })
        }
    })

})