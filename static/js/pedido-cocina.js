Array.prototype.unique=function(a){
    return function(){return this.filter(a)}}(function(a,b,c){return c.indexOf(a,b+1)<0
  });

function listarPedidos(){
    $.ajax({
        method:'get',
        // url:'/pedido/api/listDetalle',
        url:'/pedido/listaPedidos',
        success:(data)=>{
            console.log(data)
            $("#id_lista_pedidos").html('');

            var pedidos=data['pedidos']
          
             pedidos.forEach(element => {
                $("#id_lista_pedidos").append(
                    '<tr>'
                    +'<td>'+element['nombre']+'</td>'
                    +'<td class="text-center">'+element['cantidad']+'</td>'
                    +'<td class="text-center">'+element['mesa']+'</td>'
                    +'</tr>'
                    );
            });
            
        }
    })
}

listarPedidos();