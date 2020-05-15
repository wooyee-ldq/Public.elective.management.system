$(document).ready(function () {

    $("#permission").show()
    $("#blacklist .list").hide()
    $("#blacklist").hide()
    $("#blacklist .ishide").each(function (i) {
        let tid = $(this).val()
        $("#blacklist li[cid='" + tid + "']").show()
        $("#permission li[cid='" + tid + "']").hide()
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
        var tid = $(this).attr("cid")
        $.ajax({
            url: "/admin/teaAgree",
            method: "post",
            async: true,
            dataType: "json",
            data: {
                "tid": tid
            },
            success: function (msg) {
                alert(msg.tip)
                if (msg.bl == 200) {
                    $("#blacklist li[cid='" + tid + "']").hide()
                    $("#permission li[cid='" + tid + "']").show()
                }
            },
            error: function () {
                alert("解除操作失败！")
            }
        })

    });

    // 拒绝按钮点击事件
    $("#permission .refuse").click(function () {
        var tid = $(this).attr("cid")
        $.ajax({
            url: "/admin/teaRefuse",
            method: "post",
            async: true,
            dataType: "json",
            data: {
                "tid": tid
            },
            success: function (msg) {
                alert(msg.tip)
                if (msg.bl == 200) {
                    $("#permission li[cid='" + tid + "']").hide()
                    $("#blacklist li[cid='" + tid + "']").show()
                }
            },
            error: function () {
                alert("禁止操作失败！")
            }
        })

    });

})