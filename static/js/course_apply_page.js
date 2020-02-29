$(document).ready(function () {

    $("#time input").timeDropper({
        // meridians: true,   // 默认为 false
        format: 'HH:mm'
    })

    // // 反选按钮点击事件
    // $("#reverse_all").click(function(){
    //     $("#seltime :checkbox").each(function(i){
    //         $(this).prop("checked", !$(this).prop("checked"));
    //     });
    // });

    // // 全选按钮点击事件
    // $("#check_all").click(function(){
    //     $("#seltime :checkbox").prop("checked", true);
    // });

    // 设置按钮点击事件
    $("#apply").click(function () {
        var name = $("#name")
        var type = $("#type")
        var week = $("#week")
        var time = $("#time input")
        var room = $("#rid")
        var crd = $("#credit")
        var num = $("#cnum")
        let cname = name.val()
        let ctype = type.val()
        let cweek = week.val()
        let ctime = time.val()
        let rid = room.val()
        let credit = crd.val()
        let cnum = num.val()
        if (cname == "" || ctype == "" || ctime == "" || cweek == "" || rid == "" || credit == "" || cnum == "") {
            alert("字段均为必填！")
        } else {
            // alert(cname + ctype + cweek + ctime + rid + credit)
            $.ajax({
                url: "/tea/courseApply",
                method: "post",
                async: true,
                dataType: "json",
                data: {
                    "cname": cname,
                    "ctype": ctype,
                    "cweek": cweek,
                    "ctime": ctime,
                    "rid": rid,
                    "credit": credit,
                    "cnum": cnum
                },
                success: function (msg) {
                    alert(msg.tip)
                    if (msg.bl == 200) {
                        name.val("")
                    }
                },
                error: function () {
                    alert("开课申请操作失败！")
                }
            })
        }

    });

    // // 结束按钮点击事件
    // $("#over").click(function () {
    //     var cid_arr = new Array();
    //     $("#seltime input:checkbox[name='cid']:checked").each(function (i) {
    //         cid_arr[i] = $(this).val()
    //     });
    //     if (cid_arr.length <= 0) {
    //         alert("请先选择开课记录！")
    //     } else {
    //         $.ajax({
    //             url: "/admin/courseOver",
    //             method: "post",
    //             async: true,
    //             dataType: "json",
    //             data: {
    //                 "cid_arr": cid_arr.toString()
    //             },
    //             success: function (msg) {
    //                 alert(msg.tip)
    //                 if (msg.bl == 200) {
    //                     for (let i = 0; i < cid_arr.length; i++) {
    //                         $("li span[cid='" + cid_arr[i] + "']").html("是")
    //                         $("li input[cid='" + cid_arr[i] + "']").remove()
    //                     }
    //                 }
    //             },
    //             error: function () {
    //                 alert("结束开课操作失败！")
    //             }
    //         })
    //     }

    // });


})