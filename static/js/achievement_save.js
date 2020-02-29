$(document).ready(function(){

    // 保存按钮点击事件
    $("#save").click(function(){
        var achi_li = new Array();
        var error = false
        $(".grade_li").each(function(i){

            acid = $(this).attr("acid")
            isgreat = $(this).find(".isgreat select").val()
            grade = $(this).find(".grade input").val()
            if(grade != ""){
                g = Number(grade)
                if(g > 100 || g < 0 || isNaN(g)){
                    $(this).find(".grade input").val("")
                    error = true
                }else{
                    grade_li = new Array()
                    grade_li.push(acid, isgreat, grade)
                    achi_li.push(grade_li)
                }
            }
        })
        if(error){
            alert("存在无效成绩，已把该成绩清空！")
        }

        if(achi_li.length <= 0){
            alert("请至少录入一个有效成绩！")
        }else{
            $.ajax({
                url: "/tea/achievementSave",
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

    // 清空按钮点击事件
    $("#clear").click(function(){
        let bl = confirm("确认要清空所有成绩吗？")
        if(bl == true){
            $(".grade input").val("")
        }
    });

})