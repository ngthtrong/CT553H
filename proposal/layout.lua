-- Use the narrow index column in the supplied process table.
function Table(tbl)
  local first = pandoc.utils.stringify(tbl.head.rows[1].cells[1].contents)
  if first == 'STT' then
    tbl.colspecs = {{pandoc.AlignCenter, 0.07}, {pandoc.AlignLeft, 0.47}, {pandoc.AlignLeft, 0.46}}
  else
    tbl.colspecs = {{pandoc.AlignLeft, 0.25}, {pandoc.AlignLeft, 0.55}, {pandoc.AlignLeft, 0.20}}
  end
  return tbl
end
