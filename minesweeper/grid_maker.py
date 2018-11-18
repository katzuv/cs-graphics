NUM_OF_COLUMNS = 10
with open('grid.txt', 'w') as f:
    for row in xrange(NUM_OF_COLUMNS):
        for column in xrange(NUM_OF_COLUMNS):
            f.write('{}{} '.format(row, column))
        f.write('\n')
