$(document).ready(function(){

    // 保存按钮点击事件
    $("#save").click(function(){
        var achi_li = new Array();
        var error = false
        $(".grade_li").each(function(i){

            acid = $(this).attr("acid")
            isgreat = $(this).find(".isgreat select").val()
            grade = $(this).find(".grade input").val()
            grd = $(this).find(".grade input").attr("grade")
            grt = $(this).find(".isgreat").attr("isgreat")
            if(grade != grd || grt != isgreat){
                g = Number(grade)
                if(g > 100 || g < 0 || isNaN(g) || grade == ""){
                    $(this).find(".grade input").val(grd)
                    error = true
                }else{
                    grade_li = new Array()
                    grade_li.push(acid, isgreat, grade)
                    achi_li.push(grade_li)
                }
            }
        })
        if(error){
            alert("存在修改成绩为无效成绩，已把该成绩还原！")
        }

        if(achi_li.length <= 0){
            alert("请至少修改一个成绩为有效成绩！")
        }else{
            $.ajax({
                url: "/tea/achievementChange",
                method: "post",
                async: true,
                dataType: "json",
                data: {
                    "achi_li": achi_li.toString()
                },
                success: function (msg) {
                    alert(msg.tip)
                    if(msg.bl == 200){
                        location.reload(true)
                    }
                },
                error: function () {
                    alert("成绩保存失败！")
                }
            })
        }

    });

    // 还原按钮点击事件
    $("#rollback").click(function(){
        let bl = confirm("确认要还原所有成绩吗？")
        if(bl == false){
            return
        }
        $(".grade_li").each(function(i){
            grt = $(this).find(".isgreat").attr("isgreat")
            $(this).find(".isgreat select").val(grt)
            grd = $(this).find(".grade input").attr("grade")
            $(this).find(".grade input").val(grd)
        })
    });

})