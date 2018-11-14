with open('grid.txt', 'w') as f:
    for row in xrange(10):
        for column in xrange(10):
            f.write('{}{} '.format(row, column))
        f.write('\n')
