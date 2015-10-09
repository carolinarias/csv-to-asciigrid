#!/usr/bin/env python
import csv, numpy, time

def ascii_grid_from_dict(dictionary, num_rows, num_cols):
  grid = ""
  count = 0
  total = num_rows * num_cols
  for row in range(1, num_rows+1):
    for col in range(1, num_cols+1):
      grid += str(dictionary[ str(total - row*num_cols + col) ])
      count += 1
      if count % num_cols == 0 and not count == total:
        grid += '\n'
      elif not count == total:
        grid += '\t'
  return grid

grid_ncols = 100
grid_nrows = 100
grid_xllcorner = 501017.5
grid_yllcorner = 5022692.5
grid_cellsize = 235
grid_nodata = -9999

grid_num_cells = grid_ncols * grid_nrows

tsv_file = 'sms-call-internet-mi-2013-11-19.txt'

out = {}

with open(''.join(['./sources/', tsv_file]), 'rb') as telecom_data:

  telecom_data = csv.reader(telecom_data, delimiter='\t')
  count = 0

  print "Start parsing data..."

  for row in telecom_data:

    # 0: sid
    # 1: timestamp
    # 2: country_code
    # 3: messages_in
    # 4: messages_out
    # 5: calls_in
    # 6: calls_out
    # 7: internet_traffic

    sid = row[0]
    ts = row[1][0:10]
    messages_in = row[3]

    # Check empty values and convert values to double
    if messages_in == '':
      messages_in = numpy.longdouble(0.0)
    elif type(messages_in) is str:
      messages_in = numpy.longdouble(messages_in)

    # Add the timestamp to the dictionary
    if ts not in out:
      out[ts] = {}
      # Initialize all the cell ids, ordered from 1 to 10000
      for sid in [str(i) for i in range(1, grid_num_cells+1)]:
        out[ts][sid] = numpy.longdouble(0.0)

    # Add the cell id to the dictionary
    if sid not in out[ts]:
      out[ts][sid] = numpy.longdouble(0.0)

    # Add values with same timestamp and same cell id
    out[ts][sid] += messages_in
    
    count += 1

    # Give feedback
    if count < 10000 and count % 1000 == 0:
      print 'Parsed', count, 'records'
    elif count % 100000 == 0:
      print 'Parsed', count, 'records'
print ""
# Give feedback again
print 'Finished parsing data. There are', len(out.keys()), 'timestamps.'
print 'Writing', len(out.keys()), 'grid files...'

# Grid headers
grid_header = 'ncols %d\n' % grid_ncols
grid_header += 'nrows %d\n' % grid_nrows
grid_header += 'xllcorner %s\n' % grid_xllcorner
grid_header += 'yllcorner %s\n' % grid_yllcorner
grid_header += 'cellsize %s\n' % grid_cellsize
grid_header += 'NODATA_value %d\n' % grid_nodata

# Write the grid files
for ts in out.keys():

  count = 0

  assert len(out[ts]) == grid_num_cells

#  print out[ts]

  grid_values = ascii_grid_from_dict( out[ts], grid_ncols, grid_nrows )
  
  # grid_values = ''
  # for sid in out[ts].keys():
  # # for sid in [str(i) for i in range(1,10001)]:
  #   grid_values += '%s' % out[ts][sid]

  #   count += 1
  #   if count % grid_ncols == 0 and not count == grid_num_cells:
  #     grid_values += '\n'
  #   elif not count == grid_num_cells:
  #     grid_values += '\t'
  
  filename = ''.join(['./grids/', ts, '.asc'])
  f = open(filename, 'w')
  f.write(grid_header)
  f.write(grid_values)
  f.close()

# Bye!
print "Done. Enjoy your grids."
