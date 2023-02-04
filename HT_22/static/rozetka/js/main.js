$(function () {
    // popovers
    $('[data-toggle="popover"]').popover()

    //Adding a product to the cart
    $("#add").submit(function (e) {
        // preventing from page reload and default actions
        e.preventDefault();
        // serialize the data for sending the form data.
        const serializedData = $(this).serialize();
        // make POST ajax call
        $.ajax({
            type: "POST",
            url: $("#add").attr("action"),
            data: serializedData,
            success: function (response) {
                console.log(response);
                $("#count_item").text(response.qty);
            },
            error: function (response) {
                // alert the error if any error occured
                alert(response["responseJSON"]["error"]);
            }
        })
    })

    //Removing the product from the cart
    $(document).on("click","#remove-item", function (event) {
        // preventing from page reload and default actions
        event.preventDefault();

        let pid = $(this).attr("data-pid");
        let total = $("#total-price").val()
        // make GET ajax call
        $.ajax({
            type: "GET",
            url: "/cart/remove/",
            data: {
                "product_id": pid,
            },
            success: function (response) {
                console.log(response);
                $( "#cart-item" + pid ).remove();
                $("#count_item").text(response.qty);
                $("#total-price").text(response.total_price);
            },
            error: function (response) {
                // alert the error if any error occured
                alert(response["responseJSON"]["error"]);
            }
        })
    })

    //Clearing cart
    $(document).on("click","#clear-cart", function (event) {
        // preventing from page reload and default actions
        event.preventDefault();
        // make GET ajax call
        $.ajax({
            type: "GET",
            url: "/cart/clear/",
            success: function (response) {
                console.log(response);
                $( "#body-cart").remove();
                $("#count_item").text("0");
                $("#total-price").text(response.total_price);
            },
            error: function (response) {
                // alert the error if any error occured
                alert(response["responseJSON"]["error"]);
            }
        })
    })
})