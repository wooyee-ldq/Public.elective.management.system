$(document).ready(function(){

    // 反选按钮点击事件
    $("#reverse_all").click(function(){
        $("#course :checkbox").each(function(i){
            $(this).prop("checked", !$(this).prop("checked"));
        });
    });

    // 全选按钮点击事件
    $("#check_all").click(function(){
        $("#course :checkbox").prop("checked", true);
    });

    // 结课按钮点击事件
    $("#refuse").click(function(){
        let bl = confirm("确认要结束选择的课程吗？")
        if(bl == false){
            return
        }
        var cid_arr = new Array();
        $("#course input:checkbox[name='cid']:checked").each(function(i){
            cid_arr[i] = $(this).val()
        });
        if(cid_arr.length <= 0){
            alert("请先选择课程！")
        }else{
            $.ajax({
                url: "/tea/teaCourseEnd",
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
                            $("#course li[cid='" + cid_arr[i] + "']").remove()
                        }
                    }
                },
                error: function () {
                    alert("结课操作失败！")
                }
            })
        }

    });

})