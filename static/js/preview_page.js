$(document).ready(function(){

    $("#pre").find("div").each(function(){
        cid = $(this).attr("cid")
        $("#course button[cid="+cid+"]").hide()
    })

    // 添加按钮点击事件
    $(".add").click(function(){
        pre_size = $("#pre").find("div").length
        if(pre_size >= 3){
            alert("最多预选3个课程！")
            return
        }
        cid = $(this).attr("cid")
        prediv = '<div cid="'+cid+'">' 
        + $("li[cid="+cid+"]").find(".cname").text() 
        + '<button class="btn btn-danger del" cid="'+cid+'">删除</button></div>'
        $("#pre").append(prediv)
        $(this).hide()
    })

    // 删除按钮点击事件
    $("#pre").on('click', 'button', function(){
        cid = $(this).attr("cid")
        $("button[cid="+cid+"]").show()
        $(this).parent().remove()
    })


    // 预选提交按钮点击事件
    $("#preview").click(function(){
        var cid_li = new Array();
        $("#pre").find("div").each(function(){
            cid = $(this).attr("cid")
            cid_li.push(cid)
        })
        if(cid_li.length <= 0){
            alert("请先添加课程！")
        }else{
            $.ajax({
                url: "/stu/preview",
                method: "post",
                async: true,
                dataType: "json",
                data: {
                    "cid_li": cid_li.toString()
                },
                success: function (msg) {
                    alert(msg.tip)
                },
                error: function () {
                    alert("预选课程失败！")
                }
            })
        }

    });

})