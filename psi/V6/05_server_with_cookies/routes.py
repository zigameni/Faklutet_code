from controllers import index, results, add_proizvod, view_add_proizvod, view_cart

routes = {
    '/': index,
    '/results': results,
    '/add-proizvod': add_proizvod,
    '/view-add-proizvod': view_add_proizvod,
    '/view-cart' : view_cart
};
