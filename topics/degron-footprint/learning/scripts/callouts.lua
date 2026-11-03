-- Preserve the educational role of each box in the rendered learning guide.
local colors = {
  concept='teal', worked='blue', choice='teal', evidence='teal',
  limit='amber', roadmap='amber', exercise='blue'
}

function Div(el)
  for _, class in ipairs(el.classes) do
    if colors[class] then
      local title = pandoc.write(pandoc.Pandoc({pandoc.Para({pandoc.Str(el.attributes.title or '')})}), 'latex'):gsub('%s+$','')
      local body = pandoc.write(pandoc.Pandoc(el.content), 'latex')
      local options = class == 'exercise' and '[breakable=false,fontupper=\\small,before skip=5pt,after skip=5pt,top=1.5mm,bottom=1.5mm]' or ''
      return pandoc.RawBlock('latex', '\\begin{learningbox}'..options..'{'..colors[class]..'}{'..title..'}\n'..body..'\n\\end{learningbox}')
    end
  end
end

function Table(el)
  local rows = 0
  for _, part in ipairs(el.bodies) do rows = rows + #part.body end
  if rows <= 10 then
    -- Small comparison tables should be readable together on one page.
    return pandoc.RawBlock('latex', '\\begin{minipage}{\\linewidth}\n'..
      pandoc.write(pandoc.Pandoc({el}), 'latex')..'\n\\end{minipage}\\par')
  end
end

function Image(el)
  -- A cap plus keepaspectratio in the template prevents tall diagrams overflowing.
  el.attributes.height = '148mm'
  if el.src:match('local%-training%-plan') then el.attributes.height = '120mm' end
  return el
end
