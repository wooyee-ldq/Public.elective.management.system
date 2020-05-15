$(document).ready(function () {

    $("#permission").show()
    $("#blacklist .list").hide()
    $("#blacklist").hide()
    $("#blacklist .ishide").each(function (i) {
        let sid = $(this).val()
        $("#blacklist li[cid='" + sid + "']").show()
        $("#permission li[cid='" + sid + "']").hide()
    })


    // 导航栏切换显示
    $("#nav li").click(function () {
        $(this).siblings("li").removeClass("active")
        $(this).addClass("active")
        $(".show").hide()
        let tip = $(this).attr("tip")
        $("#" + tip).show()
    });

    // 同意按钮点击事件
    $("#blacklist .agree").click(function () {
        var sid = $(this).attr("cid")
        $.ajax({
            url: "/admin/stuAgree",
            method: "post",
            async: true,
            dataType: "json",
            data: {
                "sid": sid
            },
            success: function (msg) {
                alert(msg.tip)
                if (msg.bl == 200) {
                    $("#blacklist li[cid='" + sid + "']").hide()
                    $("#permission li[cid='" + sid + "']").show()
                }
            },
            error: function () {
                alert("解除操作失败！")
            }
        })

    });

    // 拒绝按钮点击事件
    $("#permission .refuse").click(function () {
        var sid = $(this).attr("cid")
        $.ajax({
            url: "/admin/stuRefuse",
            method: "post",
            async: true,
            dataType: "json",
            data: {
                "sid": sid
            },
            success: function (msg) {
                alert(msg.tip)
                if (msg.bl == 200) {
                    $("#permission li[cid='" + sid + "']").hide()
                    $("#blacklist li[cid='" + sid + "']").show()
                }
            },
            error: function () {
                alert("禁止操作失败！")
            }
        })

    });

})