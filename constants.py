
axis = ['x', 'y', 'z']
placeholderGroup='tr4sh071'
placeholderAttributes = ['reference', "position", "rotation", "size"]
placeholderAllAttributes = ['reference']

for attr in placeholderAttributes[1:]:
    for ax in axis:
        placeholderAllAttributes.append("{}{}".format(attr, ax.upper()))


