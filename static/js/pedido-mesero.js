Array.prototype.unique = function (a) {
    return function () { return this.filter(a) }
}(function (a, b, c) {
    return c.indexOf(a, b + 1) < 0
});

function listarPedidos() {
    $.ajax({
        method: 'get',
        // url:'/pedido/api/listDetalle',
        url: '/pedido/listaPedidos',
        success: (data) => {
            console.log(data)
            $("#id-pedidos-mesero").html('');

            var pedidos = data['pedidos']

            pedidos.forEach(element => {
                $("#id-pedidos-mesero").append(
                    '<tr>'
                    + '<td>' + element['mesa'] + '</td>'
                    + '<td class="text-center">' + element['nombre'] + '</td>'
                    + '<td class="text-center">' + element['cantidad'] + '</td>'
                    + '<td class="text-center"><button class="btn btn-success btn-sm" onclick="entregarPedidos(' + element['pedido'] + ',' + element['producto'] + ')"><i class="fa fa-check"></i></button></td>'
                    + '</tr>'
                );
            });

        }
    })
}

listarPedidos();

function entregarPedidos(pedido, producto) {
    console.log(pedido, producto)

    $.ajax({
        method: 'post',
        url: '/pedido/delete',
        data: JSON.stringify({
            'pedido': pedido,
            'producto': producto
        }),
        success: data => {
            // $("#confirmarModal").modal('hide');
            $.ajax({
                method: 'get',
                url: 'http://localhost:3000/notificacion',
                success: () => {
                    console.log('peticion exitosa')
                    listarPedidos();
                    alert('Pedido entregado con éxito')
                }
            })


        }
    })
}