$(document).ready(function(){

    $(".show").hide()
    $("#index").show()

    // 导航栏切换显示
    $("#nav ul").on('click', 'li', function(){
        $(this).siblings("li").removeClass("active")
        $(this).addClass("active")
        $(".show").hide()
        let tip = $(this).attr("tip")   
        $("#" + tip).show()     
    });

    // 发布按钮点击事件
    $("#issue").click(function(){
        sel = $("#notice")
        let notice = sel.val()
        sel.val("")
        if(notice == "" || notice == null){
            alert("发布内容不能为空!")
        }else{
            $.ajax({
                url: "/admin/issueNotice",
                method: "post",
                async: true,
                dataType: "json",
                data: {
                    "notice": notice
                },
                success: function (msg) {
                    alert(msg.tip)
                },
                error: function () {
                    alert("发布失败！")
                }
            })
        }

    })

    // 发布公告取消按钮点击事件
    $("#cancel_issue").click(function(){
        $("#notice").val("")
    })
    
    // 修改密码取消按钮点击事件
    $("#cancel_chpwd").click(function(){
        $("#old_pwd").val("")
        $("#new_pwd1").val("")
        $("#new_pwd2").val("")
    })

    // 修改密码确认按钮点击事件
    $("#sure_chpwd").click(function(){
        let pwd = $("#old_pwd")
        let pwd1 = $("#new_pwd1")
        let pwd2 = $("#new_pwd2")
        let old_pwd = pwd.val()
        let new_pwd1 = pwd1.val()
        let new_pwd2 = pwd2.val()
        if(old_pwd == "" || new_pwd1 == "" || new_pwd2 == ""){
            alert("字段不能为空！")
        }else{
            let bl = confirm("确认修改密码？")
            if (bl == false) {
                return
            }
            pwd.val("")
            pwd1.val("")
            pwd2.val("")
            $.ajax({
                url: "/admin/changePwd",
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

     // 创建管理员取消按钮点击事件
     $("#cancel_add").click(function(){
        $("#ano").val("")
        $("#pwd").val("")
    })

    // 创建管理员确认按钮点击事件
    $("#sure_add").click(function(){
        let user = $("#ano")
        let pwd = $("#pwd")
        let username = user.val()
        let password = pwd.val()
        if(username == "" || password == ""){
            alert("字段不能为空！")
        }else{
            user.val("")
            pwd.val("")
            $.ajax({
                url: "/admin/createAdmin",
                method: "post",
                async: true,
                dataType: "json",
                data: {
                    "username": username,
                    "password": password
                },
                success: function (msg) {
                    alert(msg.tip)
                },
                error: function () {
                    alert("创建失败！")
                }
            })
        }
    })

    // 快速创建普通管理员按钮点击事件
    $("#fast_add").click(function(){
        $.ajax({
            url: "/admin/fastCreateAdmin",
            method: "post",
            async: true,
            dataType: "json",
            data: {},
            success: function (msg) {
                alert(msg.tip)
            },
            error: function () {
                alert("创建失败！")
            }
        })
    })

})