-- Conserva el número de las ecuaciones: pandoc descarta \tag{} al convertir a OMML.
function Math(el)
  if el.mathtype == "DisplayMath" and el.text:find([[\tag]], 1, true) then
    el.text = el.text:gsub([[\tag%s*{([^}]*)}]], [[\qquad\qquad(%1)]])
  end
  return el
end
