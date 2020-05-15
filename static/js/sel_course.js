$(document).ready(function(){

    $("#pre").find("div").each(function(){
        cid = $(this).attr("cid")
        $("#course button[cid="+cid+"]").hide()
    })

    $("#sel_course").find("div").each(function(){
        cid = $(this).attr("cid")
        $("#course button[cid="+cid+"]").hide()
    })

    // 添加按钮点击事件
    $(".add").click(function(){
        pre_size = $("#pre").find("div").length
        sel_size = $("#sel_course").find("div").length
        if(pre_size + sel_size >= 3){
            alert("最多选择3个课程！")
            return
        }
        cid = $(this).attr("cid")
        prediv = '<div cid="'+cid+'"><span>' 
        + $("li[cid="+cid+"]").find(".cname").text() 
        + '</span><button class="btn btn-danger del" cid="'+cid+'">删除</button></div>'
        $("#pre").append(prediv)
        $(this).hide()
    })

    // 删除按钮点击事件
    $("#pre").on('click', 'button', function(){
        cid = $(this).attr("cid")
        $("button[cid="+cid+"]").show()
        $(this).parent().remove()
    })


    // 选课提交按钮点击事件
    $("#sel").click(function(){
        var cid_li = new Array();
        $("#pre").find("div").each(function(){
            cid = $(this).attr("cid")
            cid_li.push(cid)
        })
        if(cid_li.length <= 0){
            alert("请先添加课程！")
        }else{
            $.ajax({
                url: "/stu/selCourse",
                method: "post",
                async: true,
                dataType: "json",
                data: {
                    "sel_li": cid_li.toString()
                },
                success: function (msg) {
                    if(msg.bl == 200){
                        var str = ""
                        for(let i = 0; i < msg.tip.length; i++){
                            cid = msg.tip[i]
                            seldiv = $("#pre div[cid="+cid+"]")
                            // seldiv.find("button").remove()
                            str = str + "《" + seldiv.text() + "》 "
                            seldiv.find("button").removeClass("del").addClass("remove").text("退选")
                            $("#sel_course").append(seldiv)
                            if(i == msg.tip.length-1){
                                alert(str + "选课成功，选课成功4小时内可以退选!")
                            }
                        }
                    }
                    $("#pre div").remove()
                },
                error: function () {
                    alert("选课提交失败！")
                }
            })
        }

    });

    // 退选按钮点击事件
    $("#sel_course").on('click', 'button', function(){
        bl = confirm("确认要退选课程：《" + $(this).parent().find("span").text() + "》吗？")
        cid = $(this).attr("cid")
        if(bl){
            $.ajax({
                url: "/stu/selRemove",
                method: "post",
                async: true,
                dataType: "json",
                data: {
                    "cid": cid
                },
                success: function (msg) {
                    alert(msg.tip)
                    if(msg.bl == 200){
                        $("#sel_course div[cid="+cid+"]").remove()
                        $("#course button[cid="+cid+"]").show()
                    }
                },
                error: function () {
                    alert("退课失败！")
                }
            })
        }
    })

})