$(document).ready(function () {

    // 反选按钮点击事件
    $("#reverse_all").click(function () {
        $("#notice :checkbox").each(function (i) {
            $(this).prop("checked", !$(this).prop("checked"));
        });
    });

    // 全选按钮点击事件
    $("#check_all").click(function () {
        $("#notice :checkbox").prop("checked", true);
    });

    // 过期设置按钮点击事件
    $("#over").click(function () {
        var cid_arr = new Array();
        $("#notice input:checkbox[name='cid']:checked").each(function (i) {
            cid_arr[i] = $(this).val()
        });
        if (cid_arr.length <= 0) {
            alert("请先选择公告记录！")
        } else {
            let bl = confirm("确认把选择的公告设置为过期吗？")
            if (bl == false) {
                return
            }
            $.ajax({
                url: "/admin/noticeOver",
                method: "post",
                async: true,
                dataType: "json",
                data: {
                    "cid_arr": cid_arr.toString()
                },
                success: function (msg) {
                    alert(msg.tip)
                    if (msg.bl == 200) {
                        for (let i = 0; i < cid_arr.length; i++) {
                            $("li span[cid='" + cid_arr[i] + "']").html("是")
                            $("li input[cid='" + cid_arr[i] + "']").remove()
                        }
                    }
                },
                error: function () {
                    alert("过期设置操作失败！")
                }
            })
        }

    });

})