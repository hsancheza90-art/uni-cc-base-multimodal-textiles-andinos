-- Ecuaciones numeradas para Word. pandoc descarta \tag{} al convertir a OMML.
-- 1) Si un párrafo contiene solo una ecuación con \tag{n}, se convierte en un párrafo de estilo
--    «Ecuacion» con la fórmula centrada y el número «(n)» alineado al margen derecho (tabuladores).
-- 2) En cualquier otro caso, el número se conserva dentro de la fórmula (\qquad\qquad(n)).

local TAB = pandoc.RawInline("openxml", "<w:r><w:tab/></w:r>")

local function es_espacio(x)
  return x.t == "Space" or x.t == "SoftBreak" or x.t == "LineBreak"
end

local function ecuacion_sola(para)
  local unica = nil
  for _, x in ipairs(para.content) do
    if x.t == "Math" and x.mathtype == "DisplayMath" then
      if unica then return nil end
      unica = x
    elseif not (es_espacio(x) or (x.t == "Str" and x.text:match("^[%.,;:]$"))) then
      return nil
    end
  end
  return unica
end

local function Para(el)
  local m = ecuacion_sola(el)
  if not m or not m.text:find([[\tag]], 1, true) then return nil end
  local numero = m.text:match([[\tag%s*{([^}]*)}]])
  local formula = m.text:gsub([[\tag%s*{[^}]*}]], "")
  -- signo de puntuación final escrito fuera de la fórmula
  local final = ""
  for _, x in ipairs(el.content) do
    if x.t == "Str" and x.text:match("^[%.,;:]$") then final = x.text end
  end
  local contenido = { TAB, pandoc.Math("InlineMath", [[\displaystyle ]] .. formula .. final), TAB,
                      pandoc.Str("(" .. numero .. ")") }
  return pandoc.Div({ pandoc.Para(contenido) }, { ["custom-style"] = "Ecuacion" })
end

local function Math(el)
  if el.mathtype == "DisplayMath" and el.text:find([[\tag]], 1, true) then
    el.text = el.text:gsub([[\tag%s*{([^}]*)}]], [[\qquad\qquad(%1)]])
  end
  return el
end

-- Primero los párrafos con una sola ecuación; después, el resto de las ecuaciones numeradas.
return { { Para = Para }, { Math = Math } }
