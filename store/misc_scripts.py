def parser(all_objects, split_by: int): #TODO: move to scripts module
    
    """Converts a list into a list of lists, each with a number of
    elements equal to "split_by". The last list is completed with
    as many elements as possible if the number of objects in the
    original list is not divisible by split_by.
    Example:
    all_objects = [1,2,3,4,5,6,7,8]
    split_by = 3
    Output: [[1,2,3], [4,5,6], [7,8]]
    """

    parsed_objects = []
    current_row = []
    counter = 0
    for object in all_objects:
        if counter < split_by:
            current_row.append(object)
            counter += 1
            if counter == split_by:
                parsed_objects.append(current_row)
                current_row = []
                counter = 0
    if current_row:
        parsed_objects.append(current_row)
    return(parsed_objects)

def compose_order_email(order,order_products,customer,
    name,telephone,email,total_cost,comment=''):   
    auxlist = []
    for producto in order_products:
        auxlist.append(str(producto))
    productos_encargados = '\n'.join(auxlist)
    
    order_details = '\n'.join([
        f'Order ID: {order.id}',
        f'Cliente: {customer}',
        f'Productos encargados:',
        f'{productos_encargados}',
        f'Valor total: {total_cost}',
        '\n',
        'Datos proporcionados en formulario web:',
        f'Nombre: {name}',
        f'Teléfono: {telephone}',
        f'Email: {email}',
        f'Comentario: {comment}',
    ])
    return order_details

def compose_contact_email(name, comment, telephone = '', email = ''):
    consulta = '\n'.join([
        '¡Llegó una consulta!',
        'Datos proporcionados en formulario web:',
        f'Nombre: {name}',
        f'Teléfono: {telephone}',
        f'Email: {email}',
        f'Comentario: {comment}',
    ])
    return consulta

#self testing
if __name__ == '__main__':
    testlist1 = [i for i in range(20)] 
    testlist2 = [3]
    testlist3 = []
    testlist4 = [1,2,[3,4],[5]]
    split_bys = [2,3,4,5,6,7,8,10,100]

    print(f'Parsing {testlist1}:')
    for item in split_bys:
        result = parser(testlist1,item)
        print(f'Splitting by {item}')
        print(result)
        print('COMPLETE')

    print()
    print(f'Parsing {testlist4}:')
    for item in split_bys:
        result = parser(testlist4,item)
        print(f'Splitting by {item}')
        print(result)
        print()

    