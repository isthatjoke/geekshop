window.onload = function () {
    let _quantity, _price, orderitem_num, delta_quantity, orderitem_quantity, delta_cost;
    let quantity_arr = [];
    let price_arr = [];
    let TOTAL_FORMS = parseInt($('input[name="orderitems-TOTAL_FORMS"]').val());
    let order_total_quantity = parseInt($('.order_total_quantity').text()) || 0;
    let order_total_cost = parseFloat($('.order_total_cost').text()) || 0;

    for (let i=0; i<TOTAL_FORMS; i++) {
        _quantity = parseInt($('input[name="orderitems-' + i + '-quantity"]').val());
        _price = parseFloat($('.orderitems-' + i + '-price').text());
        quantity_arr[i] = _quantity;
        if (_price) {
            price_arr[i] = _price;
        } else {
            price_arr[i] = 0;
        }
    }

    if (!order_total_quantity) {
        orderSummaryRecalc();
}



    if (!order_total_quantity) {
        TOTAL_FORMS = parseInt($('input[name="orderitems-TOTAL_FORMS"]').val());
        for (let i=0; i<TOTAL_FORMS; i++) {
            order_total_quantity += quantity_arr[i];
            order_total_cost += quantity_arr[i] * price_arr[i];
        }
        $('.order_total_quantity').html('Total Quantity: ' + order_total_quantity.toString());
        $('.order_total_cost').html('Total Cost: ' + Number(order_total_cost.toFixed(2)).toString() + '$');
    }

    $('.order_form').on('click', 'input[type="number"]', function () {
        let target = event.target;
        orderitem_num = parseInt(target.name.replace('orderitems-', '').replace('-quantity', ''));
        if (price_arr[orderitem_num]) {
            orderitem_quantity = parseInt(target.value);
            delta_quantity = orderitem_quantity - quantity_arr[orderitem_num];
            quantity_arr[orderitem_num] = orderitem_quantity;
            orderSummaryUpdate(price_arr[orderitem_num], delta_quantity);
        }
    });

    // $('.order_form').on('click', 'input[type="checkbox"]', function () {
    //     let target = event.target;
    //     orderitem_num = parseInt(target.name.replace('orderitems', '').replace('-DELETE', ''));
    //     if (target.checked) {
    //         delta_quantity = -quantity_arr[orderitem_num];
    //     } else {
    //         delta_quantity = quantity_arr[orderitem_num];
    //     }
    //     orderSummaryUpdate(price_arr[orderitem_num], delta_quantity);
    //     });

    $('.order_form select').change(function (e) {
    let target = e.target;
    orderitem_num = parseInt(target.name.replace('orderitems-', '').replace('-game', ''));
    let orderitem_game_pk = target.options[target.selectedIndex].value;

    if (orderitem_game_pk) {
        $.ajax({
            url: "/order/game/" + orderitem_game_pk + "/price/",
            success: function (data) {
                if (data.price) {
                    price_arr[orderitem_num] = parseFloat(data.price);
                    if (isNaN(quantity_arr[orderitem_num])) {
                        quantity_arr[orderitem_num] = 0;
                    }
                    let price_html = '<span>' + data.price.toString() + '</span> $';
                    let current_tr = $('.order_form table').find('tr:eq(' + (orderitem_num + 1) + ')');
                    current_tr.find('td:eq(2)').html(price_html);

                    if (isNaN(current_tr.find('input[type="number"]').val())) {
                        current_tr.find('input[type="number"]').val(0);
                    }
                    orderSummaryRecalc();
                }
            },
        });
    }
});

    function orderSummaryUpdate(orderitem_price, delta_quantity) {
        delta_cost = orderitem_price * delta_quantity;
        order_total_cost = Number((order_total_cost + delta_cost).toFixed(2));
        order_total_quantity = order_total_quantity + delta_quantity;

        $('.order_total_quantity').html('Total Quantity: ' + order_total_quantity.toString());
        $('.order_total_cost').html('Total Cost: ' + Number(order_total_cost.toFixed(2)).toString() + ' $');
    }

    $('.formset_row').formset({
        addText: 'add games',
        deleteText: 'remove',
        prefix: 'orderitems',
        removed: deleteOrderItem
    });

    function deleteOrderItem(row) {
        let target_name = row[0].querySelector('input[type=number]').name;
        orderitem_num = parseInt(target_name.replace('orderitems-', '').replace('-quantity', ''));
        delta_quantity = -quantity_arr[orderitem_num];
        quantity_arr[orderitem_num] = 0;
        if (!isNaN(price_arr[orderitem_num]) && !isNaN(delta_quantity)) {
            orderSummaryUpdate(price_arr[orderitem_num], delta_quantity);
        }
    }

    function orderSummaryRecalc() {
        TOTAL_FORMS = parseInt($('input[name="orderitems-TOTAL_FORMS"]').val());
        order_total_quantity = 0;
        order_total_cost = 0;

        for (let i=0; i < TOTAL_FORMS; i++) {
            order_total_quantity += quantity_arr[i];
            order_total_cost += quantity_arr[i] * price_arr[i];
        }
        $('.order_total_quantity').html('Total Quantity: ' + order_total_quantity.toString());
        $('.order_total_cost').html('Total Cost: ' + Number(order_total_cost.toFixed(2)).toString() + ' $');
    }
}



