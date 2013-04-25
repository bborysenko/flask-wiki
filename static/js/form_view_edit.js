jQuery.expr[":"].contains = function( elem, i, match, array ) {
    return (elem.textContent || elem.innerText || jQuery.text( elem ) || "").toLowerCase().indexOf(match[3].toLowerCase()) >= 0;
}


function add_user_view(){  
    id = $(this).attr('id')
    login = $(this).attr('login');
    elem = $( '<div class="right_user" id="' + id + '" login="' + login + '">' + $(this).text() + '</div>' ).bind('click', remove_user_view);
    $('div#dialog_view div.right_users_panel').append( elem );
    $(this).remove();
  }

function remove_user_view(){
    id = $(this).attr('id');
    login = $(this).attr('login');
    elem = $( '<div class="left_user" id="' + id + '" login="' + login + '">' + $(this).text() + '</div>' ).bind('click', add_user_view);
    $('div#dialog_view div.left_users_panel').append(elem);
    $(this).remove();
  }

$(document).ready(
    function(){

        $('div#dialog_view div.left_users_panel > div.left_user').each(
            function(index, elem){
                $(this).bind( 'click', add_user_view );
            }
        );
        $('div#dialog_view div.right_users_panel > div.right_user').each(
            function(index, elem){
                $(this).bind( 'click', remove_user_view );
            }
        );
    }
);

var $dialog;
var load_users_edit = false;
$(document).ready(function(){
	$dialog = $('#dialog_view').dialog({
                                    autoOpen: false,
                                    title: 'Права на просмотр',
                                    modal: true, 
                                    buttons: {
                                            "OK": function() {
                                                // очищаю содержимое тегов
                                                $('#access_show').tagit('removeAll');
                                                // добавляю новое содержимое
                                                $('div#dialog_view div.right_users_panel > div.right_user').each(
                                                     function() {
                                                        login = $(this).attr('login');
                                                        name = $(this).text();
                                                        result = name;
                                                        $('#access_show').tagit('createTag', result);    
                                                     }
                                                );
                                                $(this).dialog('close');
                                        },
                                        "Cancel": function() {
                                            $(this).dialog("close");
                                        }
                                    }   
                                }
                            );
    $dialog.dialog( "option", "width", 820 );
    $dialog.dialog( "option", "height", 400 );

    // Открытие дилогового окна
    $('#add_users_show').click(
        function (){
//            console.log('tut');
            if( !load_users_edit ){
                load_user = true;
                $('#all_users > div').each(                        
                    function(index, elem){
                        id = $(this).attr('id');
                        login = $(this).attr('login');
                        e = $( '<div class="left_user" id="' + id + '" login="' + login + '">' + $(this).text() + '</div>' ).bind('click', add_user_view);
                        $('div#dialog_view div.left_users_panel').append( e );
                        $(this).bind( 'click', remove_user_view );                            
                    }                                                                  
                );
                
                $('div#dialog_view div.right_users_panel >  div.right_user').remove();
                // добавляю в правую панель выбранных пользователей 
                $('#access_show_block li span.tagit-label').each(
                    function(){
                        name = $(this).text();
                        if(name == ""){
                            return;
                        }
                        // Поиск существующих пользователей во всех пользовтелеях
                        $('div#all_users > div:contains("' + name +  '")').each(
                            function(){
                                var id = $(this).attr('id');          
                                var login = $(this).attr('login');
                                e = $( '<div class="right_user" id="' + id + '" login="' + login + '">' + $(this).text() + '</div>' ).bind('click', remove_user_view);
                                $('div#dialog_view div.right_users_panel').append(e);        
                            }
                        ); 
                    }
                );
            }
            $dialog.dialog('open');
            $('div#dialog_view #left_panel_search').blur();
            return false; ////cancel eventbubbeling
        }
    );
});

function sravnenie_panel_view(){
   $('div#dialog_view div.right_users_panel > div.right_user').each(
       function(){        
          id = $(this).attr('id');
          $('div#dialog_view div.left_users_panel > div').each( 
            function(){//.remove();/*
              i = $(this).attr('id');
              if( i == id ){
                $(this).remove();
              }
            }
          );
      }
    );
}

function left_search_view(){
    var id = $(this).attr('id');          
    var login = $(this).attr('login');
    e = $( '<div class="left_user" id="' + id + '" login="' + login + '">' + $(this).text() + '</div>' ).bind('click', add_user_view);
    $('div#dialog_view div.left_users_panel').append(e);        
    $(this).bind( 'click', remove_user_view );
}

$(document).ready( function(){
   $('div#dialog_view #left_panel_search').keyup(
        function() {
            $('div#dialog_view div.left_users_panel > div').remove();
            $('div#all_users > div:contains("' + $(this).val() +  '")').each(left_search_view);
            sravnenie_panel_view();      
        }
    );
});

$(document).ready( function(){
    $("form").submit(
        function() {
            var arr_login = [];
            $('#access_show_block li span.tagit-label').each(
                function(){
                    name = $(this).text();
                    if(name == ""){
                        return;
                    }
                    // Поиск существующих пользователей во всех пользовтелеях
                    $('div#all_users > div:contains("' + name +  '")').each(
                        function(){
                            var id = $(this).attr('id');          
                            var login = $(this).attr('login');
                            arr_login.push(login);
                        }
                    ); 
                }
            );
            $('#form_page').css("display","none")
            $('#access_show').tagit('removeAll');
            for(i = 0; i < arr_login.length; i++){
                $('#access_show').tagit('createTag', arr_login[i]);
            }
        }
    );
});
$(document).ready(                                                             
    function(){                                             
//        $('#all_users').prepend('<div id="-1" login="all"><div class="user_data">All</div></div>');
// произвожу замену имени         
        var arr_name = [];
        $('#access_show_block li span.tagit-label').each(
            function(){
                login = $(this).text();
                if(login == ""){
                    return;
                }
                // Поиск существующих пользователей во всех пользовтелеях
                $('div#all_users > div').each(
                    function(){
                        var id = $(this).attr('id');          
                        l = $(this).attr('login');
                        if( l != login ){
                            return;
                        }
                        var name = $(this).text();
                        arr_name.push(name);
                    }
                ); 
            }
        );
        
        $('#access_show').tagit('removeAll');
        for(i = 0; i < arr_name.length; i++){
            $('#access_show').tagit('createTag', arr_name[i]);
        }
        var text = "Поиск...";                                                 
        $('div#dialog_view #left_panel_search').val(text);                          
        $('div#dialog_view #left_panel_search').focus(                              
            function(){                                                        
                $(this).addClass("active");                                    
                if($(this).attr("value") == text){                             
                    $(this).attr("value", "");                                 
                }                                                              
            }                                                                  
        );                                                                     
        $('div#dialog_view #left_panel_search').blur(                               
            function(){                                                        
                $(this).removeClass("active");                                 
                if($(this).attr("value") == "") $(this).attr("value", text);   
            }                                                                  
        );                         
    
    }                                                                                                                                        
) ; 
