document.addEventListener("DOMContentLoaded", function (event) {
  function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}





  if (document.querySelector("#all_orders_div")) {
    const all_order_buttons = document.querySelectorAll("#all_order_button");

    all_order_buttons.forEach((button) => {
      button.addEventListener("click", (event) => {
        
        fetch(`/order_deal/${event.target.dataset.action}`, {
          method: "POST",
          headers: {'X-CSRFToken': getCookie('csrftoken')},
          body: JSON.stringify({
            id: event.target.dataset.order_id,
            owner:event.target.dataset.owner
          })
        }).then((response)=>response.json()).then(reply=>{
          
          if (reply.status=='true'){
            window.open("wallet","_self")
            document.querySelector("#message_display").style.display = "block";
            document.querySelector("#message_content").innerHTML=reply.message
            
          }else{
            document.querySelector("#message_display").style.display = "block";
            document.querySelector("#message_content").innerHTML=reply.message
          }
            
          }      
      
        
      )




      });
    });
  }

  if (document.querySelector("#my_orders_div")) {
    const my_order_buttons = document.querySelectorAll("#my_order_button");
    my_order_buttons.forEach((button) => {
      button.addEventListener("click", (event) => {

        fetch(`/order_deal/close`, {
          method: "POST",
          headers: {'X-CSRFToken': getCookie('csrftoken')},
          body: JSON.stringify({
            id: event.target.dataset.order_id,
            owner:event.target.dataset.owner
          })
        }).then((response)=>response.json()).then(reply=>{
          
          if (reply.status=='true'){
            window.open("my_orders","_self")
            
            
            
          }else{
            document.querySelector("#message_display").style.display = "block";
            document.querySelector("#message_content").innerHTML=reply.message
          }
            
          }      
      
        
      )
      });
    });




  }
});
