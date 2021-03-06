﻿/* EasySlider.js modifié */

(function($) {

    $.fn.easySlider = function(options){

        var defaults = {            
            prevId:         'prevBtn',
            nextId:         'nextBtn',    
            firstId:         'firstBtn',
            lastId:         'lastBtn',    
            vertical:        false,
            speed:             800,
            auto:            false,
            pause:            2000,
            continuous:        false,
            goToButtonId:   'goToButton',
            goToRotateAmount:8,
            effect: 'Slide',
            navigation_type: 'Navigation Buttons',
            fadeNavigation:  false
        }; 
        
        var options = $.extend(defaults, options);  
                
        this.each(function() {  
            var obj = $(this);                 
            var s = $("li", obj).length;
            var w = $("li", obj).width(); 
            var h = $("li", obj).height(); 
            var timeout;
            var timer_activated = options.auto;
            obj.width(w); 
            obj.height(h); 
            obj.css("overflow","hidden");
            var ts = s-1;
            var t = 0;
            $("ul", obj).css('width',s*w);            
            if(!options.vertical) $("li", obj).css('float','left');
            
            
            //Navigation...
            if(options.navigation_type != "No Buttons"){
                var html = '';
                if(options.navigation_type == "Navigation Buttons"){
                    html += "<div id='easySlider-goToButtons'>";
                    html += ' <span id="leftb"><a class="leftright" href=\"javascript:void(0);\">&nbsp</a></span>';
                    for(var i=0; i < ts+1; i++){ 
                        html += "<a id=\"" + options.goToButtonId + i + "\" href=\"javascript:void(0);\">" + (i+1) + "</a> ";
                    }
                    html += ' <span id="rightb"><a class="leftright" href=\"javascript:void(0);\">&nbsp</a></span>';
                    html += '<div id="pauseplay"></div>';
                    html += "</div>";
                }
                if(options.navigation_type == "Big Arrows"){
                    html += ' <span id="'+ options.prevId +'"><a href=\"javascript:void(0);\">&nbsp</a></span>';
                    html += ' <span id="'+ options.nextId +'"><a href=\"javascript:void(0);\">&nbsp</a></span>';
                }else if(options.navigation_type == "Small Arrows"){
                    html += "<div id='smallButtons'>";
                    html += ' <span id="'+ options.prevId +'"><a href=\"javascript:void(0);\">&nbsp</a></span>';
                    html += ' <span id="'+ options.nextId +'"><a href=\"javascript:void(0);\">&nbsp</a></span>';
                    html += "</div>";
                }
                $(obj).after(html);                                        
            };
            //end nav
            
            $("a","#"+options.nextId).click(function(){        
                animate("next",true);
            });
            $("a","#"+options.prevId).click(function(){        
                animate("prev",true);                
            });    
            $("span#leftb a").click(function(){        
                animate("prev",true);                
            });
            $("span#rightb a").click(function(){        
                animate("next",true);                
            });
            $("a","#"+options.firstId).click(function(){        
                animate("first",true);
            });                
            $("a","#"+options.lastId).click(function(){        
                animate("last",true);                
            });    
            $("div#easySlider-goToButtons a:not(.leftright)").click(function(){
                animate(parseInt($(this).attr('id').substring(options.goToButtonId.length)), true);
            });
            
            if(options.navigation_type == "Navigation Buttons") $("#" + options.goToButtonId + "0").addClass('active');
            
            function update_goToButtons(btns){
                if(btns.size() > options.goToRotateAmount){
                    var min = Math.max(t - Math.floor(options.goToRotateAmount/2), 0);
                    var max = Math.min(t + Math.floor(options.goToRotateAmount/2), btns.size());
                    var diff = max - min;
                    if(diff != options.goToRotateAmount) min = Math.max(min - (options.goToRotateAmount - diff), 0);
                    diff = max - min;
                    if(diff != options.goToRotateAmount) max = Math.min(max + (options.goToRotateAmount - diff), btns.size());
                    for(var i = 0; i < min; i++) $("#" + options.goToButtonId + i).hide();
                    for(var i = min; i < max; i++) $("#" + options.goToButtonId + i).show();
                    for(var i = max; i < btns.size(); i++) $("#" + options.goToButtonId + i).hide();
                }
            }
            
            update_goToButtons($("div#easySlider-goToButtons a:not(.leftright)"));
            
            function animate(dir,clicked){
                var ot = t;                
                switch(dir){
                    case "next":
                        t = (ot>=ts) ? (options.continuous ? 0 : ts) : t+1;                        
                        break; 
                    case "prev":
                        t = (t<=0) ? (options.continuous ? ts : 0) : t-1;
                        break; 
                    case "first":
                        t = 0;
                        break; 
                    case "last":
                        t = ts;
                        break; 
                    default:
                        if(typeof(dir) == "number") t = dir;
                        break; 
                };    
                
                if(options.navigation_type == "Navigation Buttons"){
                    var btns = $("div#easySlider-goToButtons a:not(.leftright)");
                    btns.removeClass("active");
                    $("#" + options.goToButtonId + t).addClass('active');
                    update_goToButtons(btns);
                }
                
                var diff = Math.abs(ot-t);
                //var speed = diff*options.speed; //don't like this... too slow for lots of slides
                var position = (t*w*-1);
                if(options.vertical){
                    position = (t*h*-1);
                }
                
                if(options.effect == "Slide"){
                    var speed = (diff*options.speed)/diff;
                    if(!options.vertical) {
                        $("ul",obj).animate(
                            { marginLeft: position }, 
                            speed
                        );                
                    } else {
                        p = (t*h*-1);
                        $("ul",obj).animate(
                            { marginTop: position }, 
                            speed
                        );                    
                    };
                }else if(options.effect == "Fade"){
                    var margin = "marginLeft";
                    if(options.vertical){ margin = "marginTop"; }

                    $("ul", obj).fadeOut(Math.ceil(options.speed/2), function(){
                        $(this).css(margin, position).fadeIn(Math.ceil(options.speed/2));
                    });
                }
                
                if(!options.continuous){                    
                    if(t==ts){
                        $("a","#"+options.nextId).hide();
                        $("a","#"+options.lastId).hide();
                    } else {
                        $("a","#"+options.nextId).show();
                        $("a","#"+options.lastId).show();                    
                    };
                    if(t==0){
                        $("a","#"+options.prevId).hide();
                        $("a","#"+options.firstId).hide();
                    } else {
                        $("a","#"+options.prevId).show();
                        $("a","#"+options.firstId).show();
                    };                    
                };                
                
                if(clicked){ clear_timer() }
                if(timer_activated && dir=="next" && !clicked){
                    set_timer(diff*options.speed+options.pause);
                };
                
            };
            
            function set_timer(duration){
                timeout = setTimeout(function(){
                    animate("next",false);
                }, duration);
                timer_activated = true;
                $('div#pauseplay').addClass('pause').removeClass('play');
            }
            
            function clear_timer(){
                clearTimeout(timeout);
                timer_activated = false;
                $('div#pauseplay').addClass('play').removeClass('pause');
            }

            if(options.fadeNavigation){
                var selector = "div#smallButtons,div#easySlider-goToButtons,#" + options.prevId + ",#" + options.nextId;
                $("div#slider-container").hover(function(){
                    $(selector).fadeIn('fast');
                }, function(){
                    $(selector).fadeOut();
                });
            }

            $('div#pauseplay').click(function(){
                if(timer_activated){
                    clear_timer();
                }else{
                    set_timer(options.pause);
                }
            });
                
            // init
            if(timer_activated){
                set_timer(options.pause);
                $('div#pauseplay').addClass('pause');
            }else{
                $('div#pauseplay').addClass('play');
            }
            
            if(!options.continuous){                    
                $("a","#"+options.prevId).hide();
                $("a","#"+options.firstId).hide();                
            };                
            
        });
      
    };

})(jQuery);