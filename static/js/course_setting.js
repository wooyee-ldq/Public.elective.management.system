$(document).ready(function(){

    $.fn.datetimepicker.dates['zh-CN'] = {
        days: ["星期日", "星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"],
        daysShort: ["周日", "周一", "周二", "周三", "周四", "周五", "周六", "周日"],
        daysMin:  ["日", "一", "二", "三", "四", "五", "六", "日"],
        months: ["一月", "二月", "三月", "四月", "五月", "六月", "七月", "八月", "九月", "十月", "十一月", "十二月"],
        monthsShort: ["一月", "二月", "三月", "四月", "五月", "六月", "七月", "八月", "九月", "十月", "十一月", "十二月"],
        today: "今天",
        suffix: [],
        meridiem: ["上午", "下午"]
    }

    $(".form_datetime").datetimepicker({
        // format:'yyyy-mm-dd hh:ii:ss',  // 格式
        language:'zh-CN',  // 语言
        minuteStep:1,  // 步长
        todayBtn:true,  // 跳转到当天
        // startView: "year",  // 初始化视图是‘年’
        // minView: "month",  // 最精确视图为'月'
        // maxView: "decade",  // 最高视图为'十年'
        pickerPosition: "bottom-left",  // 显示位置
        autoclose: true,  // 选择后自动关闭
    })

    // 反选按钮点击事件
    $("#reverse_all").click(function(){
        $("#seltime :checkbox").each(function(i){
            $(this).prop("checked", !$(this).prop("checked"));
        });
    });

    // 全选按钮点击事件
    $("#check_all").click(function(){
        $("#seltime :checkbox").prop("checked", true);
    });

    // 设置按钮点击事件
    $("#set").click(function(){
        var start = $("#start input")
        var end = $("#end input")
        var mark = $("#mark")
        var campus = $("#caid")
        var level = $("#lid")
        let stime = start.val()
        let etime = end.val()
        let remark = mark.val()
        let caid = campus.val()
        let lid = level.val()
        if(stime == "" || etime == "" || remark == "" || caid == "" || lid == ""){
            alert("字段均为必填！")
        }else{
            // alert(stime + etime + remark + caid + lid)
            $.ajax({
                url: "/admin/courseSet",
                method: "post",
                async: true,
                dataType: "json",
                data: {
                    "stime": stime,
                    "etime": etime,
                    "remark": remark,
                    "caid": caid,
                    "lid": lid
                },
                success: function (msg) {
                    alert(msg.tip)
                    if(msg.bl == 200){
                        start.val("")
                        end.val("")
                        mark.val("")
                    }
                },
                error: function () {
                    alert("开课设置失败！")
                }
            })
        }

    });

    // 结束按钮点击事件
    $("#over").click(function(){
        var cid_arr = new Array();
        $("#seltime input:checkbox[name='cid']:checked").each(function(i){
            cid_arr[i] = $(this).val()
        });
        if(cid_arr.length <= 0){
            alert("请先选择开课记录！")
        }else{
            $.ajax({
                url: "/admin/courseOver",
                method: "post",
                async: true,
                dataType: "json",
                data: {
                    "cid_arr": cid_arr.toString()
                },
                success: function (msg) {
                    alert(msg.tip)
                    if(msg.bl == 200){
                        for(let i = 0; i < cid_arr.length; i++) {
                            $("li span[cid='" + cid_arr[i] + "']").html("是")
                            $("li input[cid='" + cid_arr[i] + "']").remove()
                        }
                    }
                },
                error: function () {
                    alert("结束开课操作失败！")
                }
            })
        }

    });


})