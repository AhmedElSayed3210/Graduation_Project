$(document).ready(function()
    {
        $("#diagonis").hide();
        $("#user_image").hide();
        $("#another").hide();
        $(".description1").hide();
        $(".description2").hide();
        $("#bt").on({
            click:function(){
                
                $("#dropzone").hide();
                $("#user_image").slideDown(1000);
                $("#diagonis").slideDown(1000);
                $(this).hide();
                $("#another").show();
                $(".description").hide();
                $(".description1").show();
                $(".description2").show();
                
            }
            
            
        });
         $("#another").on({
            click:function(){
                
                $("#dropzone").show();
                $("#user_image").hide();
                $("#diagonis").hide();
                $(this).hide();
                $("#bt").show();
                $(".description1").hide();
                $(".description").show();
                $(".description2").hide();
                
            }
            });
        
    });