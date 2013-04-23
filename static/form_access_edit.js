function add_user(){  
    id = $(this).attr('id')
    login = $(this).attr('login');
    elem = $( '<div class="right_user" id="' + id + '" login="' + login + '">' + $(this).text() + '</div>' ).bind('click', remove_user);
    $('div.right_users_panel').append( elem );
    $(this).remove();
  }

function remove_user(){
    id = $(this).attr('id');
    login = $(this).attr('login');
    elem = $( '<div class="left_user" id="' + id + '" login="' + login + '">' + $(this).text() + '</div>' ).bind('click', add_user);
    $('div.left_users_panel').append(elem);
    $(this).remove();
  }

$(document).ready(
    function(){
      $('div.left_users_panel > div.left_user').each(
            function(index, elem){
              $(this).bind( 'click', add_user );
            }
      );
      $('div.right_users_panel > div.right_user').each(
            function(index, elem){
              $(this).bind( 'click', remove_user );
            }
      );
    }
  );

var $dialog;
var load_users_edit = false;
$(document).ready(function(){
	$dialog = $('#dialog').dialog({
                                    autoOpen: false,
                                    title: 'Права на правку',
                                    modal: true, 
                                    buttons: {
                                            "OK": function() {
                                                $('div.right_users_panel > div.right_user').each(
                                                     function() {
                                                        login = $(this).attr('login');
                                                        name = $(this).text();
                                                        result = name;
                                                        //   result = name + "<" + login + ">"
                                                        $('#access').tagit('createTag', result);    
                                                    //      alert( $('#access_edit_block li.tagit-new text').val() );
                                                 //       $('#access_edit_block > ul text').val( result ).change()
                                             //           $('#access_edit_block > ul').prepend(element);
                                                     }
                                                );
                                                $('#access').tagit({'fieldName':'access'});
                                                $('div.right_users_panel >  div.right_user').remove();
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

    $('#add_users_edit').click(
        function (){
            if( !load_users_edit ){
                load_user = true;
                $('#all_users > div').each(                        
                    function(index, elem){
                        id = $(this).attr('id');
                        login = $(this).attr('login');
                        e = $( '<div class="left_user" id="' + id + '" login="' + login + '">' + $(this).text() + '</div>' ).bind('click', add_user);
                        $('div.left_users_panel').append( e );
                        $(this).bind( 'click', remove_user );                            
                    }                                                                  
                );
//                $('div.right_users_panel >  div.right_user').remove();
            }
            $dialog.dialog('open');
            return false; ////cancel eventbubbeling
        }
    );
});

function sravnenie_panel(){
   $('div.right_users_panel > div.right_user').each(
       function(){        
          id = $(this).attr('id');
          $('div.left_users_panel > div').each( 
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

function left_search(){
    var id = $(this).attr('id');          
    var login = $(this).attr('login');
    e = $( '<div class="left_user" id="' + id + '" login="' + login + '">' + $(this).text() + '</div>' ).bind('click', add_user);
    $('div.left_users_panel').append(e);        
    $(this).bind( 'click', remove_user );
}

jQuery.expr[":"].contains = function( elem, i, match, array ) {
    return (elem.textContent || elem.innerText || jQuery.text( elem ) || "").toLowerCase().indexOf(match[3].toLowerCase()) >= 0;
}


$('#left_panel_search').keyup(
    function() {
        $('div.left_users_panel > div').remove();
        $('div#all_users > div:contains("' + $(this).val() +  '")').each(left_search);
        sravnenie_panel();      
    }
);
