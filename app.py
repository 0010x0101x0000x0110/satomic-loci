import streamlit as st
import sys
from io import StringIO
from logic import parse, ParseError, TableauProver

st.divider()

st.header("ℹ️ Acerca de")
st.markdown("""
Sistema de lógica subatómica con tableaux semánticos.

**Características:**
- Cuantificadores universales y particulares  
- Operadores de complemento y privación  
- Conectivos proposicionales clásicos  
- Relaciones Q (ternaria) y S (binaria)

**Versión:** 1.0
""")


tab1, tab2, tab3 = st.tabs(["🧪 Probar Formula", "📜 Probar Argumento", "📚 Ejemplos"])

with tab1:
    st.header("Probar Validez de una Formula")
    st.markdown("Ingresa una formula para verificar si es valida (tautologia).")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        formula_input = st.text_input(
            "Formula:",
            value="A | -A",
            help="Escribe la formula usando la sintaxis de la guia"
        )
    
    with col2:
        prove_button = st.button("🔍 Probar", type="primary", use_container_width=True)
    
    show_steps = st.checkbox("Mostrar paso a paso", value=False)
    
    if prove_button and formula_input:
        try:
            parsed = parse(formula_input)
            
            st.markdown("### Formula Parseada")
            st.markdown(f'<div class="formula-box">{parsed}</div>', unsafe_allow_html=True)
            
            old_stdout = sys.stdout
            sys.stdout = captured_output = StringIO()
            
            prover = TableauProver(max_iterations=50)
            result = prover.prove(parsed, verbose=show_steps)
            
            sys.stdout = old_stdout
            output = captured_output.getvalue()
            
            st.markdown("### Resultado")
            
            if result:
                st.markdown(
                    '<div class="result-valid">✓ La formula es VALIDA (Tautologia)</div>',
                    unsafe_allow_html=True
                )
            else:
                st.markdown(
                    '<div class="result-invalid">✗ La formula NO es valida</div>',
                    unsafe_allow_html=True
                )
            
            if show_steps and output:
                st.markdown("### Proceso del Tableau")
                with st.expander("Ver pasos detallados", expanded=True):
                    st.text(output)
        
        except ParseError as e:
            st.error(f"❌ Error al parsear la formula: {str(e)}")
            st.info("💡 Revisa la sintaxis en la guia de la barra lateral.")
        except Exception as e:
            st.error(f"❌ Error inesperado: {str(e)}")
            st.exception(e)

with tab2:
    st.header("Probar Validez de un Argumento")
    st.markdown("Ingresa premisas y conclusion para verificar si el argumento es valido.")
    
    st.markdown("#### Premisas")
    
    num_premises = st.number_input("Numero de premisas:", min_value=1, max_value=10, value=2)
    
    premises_input = []
    for i in range(num_premises):
        default_val = "[A]B" if i == 0 else "[B]C" if i == 1 else ""
        premise = st.text_input(f"Premisa {i+1}:", key=f"premise_{i}", value=default_val)
        premises_input.append(premise)
    
    st.markdown("#### Conclusion")
    conclusion_input = st.text_input("Conclusion:", value="[A]C")
    
    col1, col2 = st.columns([3, 1])
    
    with col2:
        prove_arg_button = st.button("🔍 Probar Argumento", type="primary", use_container_width=True)
    
    show_steps_arg = st.checkbox("Mostrar paso a paso", value=False, key="show_steps_arg")
    
    if prove_arg_button:
        try:
            parsed_premises = [parse(p) for p in premises_input if p.strip()]
            parsed_conclusion = parse(conclusion_input)
            
            st.markdown("### Argumento")
            
            st.markdown("**Premisas:**")
            for i, (p_str, p_parsed) in enumerate(zip(premises_input, parsed_premises), 1):
                st.markdown(f'{i}. <div class="formula-box">{p_parsed}</div>', unsafe_allow_html=True)
            
            st.markdown(f'**Conclusion:** <div class="formula-box">{parsed_conclusion}</div>', unsafe_allow_html=True)
            
            old_stdout = sys.stdout
            sys.stdout = captured_output = StringIO()
            
            prover = TableauProver(max_iterations=50)
            result = prover.prove_argument(parsed_premises, parsed_conclusion, verbose=show_steps_arg)
            
            sys.stdout = old_stdout
            output = captured_output.getvalue()
            
            st.markdown("### Resultado")
            
            if result:
                st.markdown(
                    '<div class="result-valid">✓ El argumento es VALIDO</div>',
                    unsafe_allow_html=True
                )
            else:
                st.markdown(
                    '<div class="result-invalid">✗ El argumento NO es valido</div>',
                    unsafe_allow_html=True
                )
            
            if show_steps_arg and output:
                st.markdown("### Proceso del Tableau")
                with st.expander("Ver pasos detallados", expanded=True):
                    st.text(output)
        
        except ParseError as e:
            st.error(f"❌ Error al parsear: {str(e)}")
            st.info("💡 Revisa la sintaxis en la guia.")
        except Exception as e:
            st.error(f"❌ Error inesperado: {str(e)}")
            st.exception(e)

with tab3:
    st.header("Ejemplos de Silogismos y Formulas")
    
    st.markdown("### Silogismos Clasicos")
    
    examples = {
        "Barbara": {
            "premises": ["[M]P", "[S]M"],
            "conclusion": "[S]P",
            "description": "Todo M es P, Todo S es M ⊢ Todo S es P"
        },
        "Celarent": {
            "premises": ["-<M>P", "[S]M"],
            "conclusion": "-<S>P",
            "description": "Ningun M es P, Todo S es M ⊢ Ningun S es P"
        },
        "Darii": {
            "premises": ["[M]P", "<S>M"],
            "conclusion": "<S>P",
            "description": "Todo M es P, Algun S es M ⊢ Algun S es P"
        },
        "Ferio": {
            "premises": ["-<M>P", "<S>M"],
            "conclusion": "<S>~P",
            "description": "Ningun M es P, Algun S es M ⊢ Algun S es no-P"
        },
    }
    
    for name, example in examples.items():
        with st.expander(f"**{name}** - {example['description']}"):
            st.markdown("**Premisas:**")
            for i, p in enumerate(example['premises'], 1):
                st.code(p, language=None)
            
            st.markdown("**Conclusion:**")
            st.code(example['conclusion'], language=None)
            
            if st.button(f"Probar {name}", key=f"example_{name}"):
                try:
                    parsed_premises = [parse(p) for p in example['premises']]
                    parsed_conclusion = parse(example['conclusion'])
                    
                    with st.spinner(f"Probando {name}..."):
                        prover = TableauProver(max_iterations=50)
                        result = prover.prove_argument(parsed_premises, parsed_conclusion, verbose=False)
                    
                    if result:
                        st.success(f"✓ {name} es VALIDO")
                    else:
                        st.warning(f"✗ {name} NO es valido en este sistema")
                except Exception as e:
                    st.error(f"Error: {str(e)}")
    
    st.divider()
    
    st.markdown("### Formulas Logicas Clasicas")
    
    logic_examples = {
        "Ley del Tercero Excluido": "A | -A",
        "Ley de No Contradiccion": "-(A & -A)",
        "Modus Ponens": "(A & (A -> B)) -> B",
        "Modus Tollens": "((A -> B) & -B) -> -A",
        "Silogismo Hipotetico": "((A -> B) & (B -> C)) -> (A -> C)",
        "Dilema Constructivo": "((A -> B) & (C -> D) & (A | C)) -> (B | D)",
    }
    
    for name, formula in logic_examples.items():
        with st.expander(f"**{name}**"):
            st.code(formula, language=None)
            if st.button(f"Probar {name}", key=f"logic_{name}"):
                try:
                    parsed = parse(formula)
                    
                    with st.spinner(f"Probando {name}..."):
                        prover = TableauProver(max_iterations=50)
                        result = prover.prove(parsed, verbose=False)
                    
                    if result:
                        st.success(f"✓ {name} es VALIDO")
                    else:
                        st.warning(f"✗ {name} NO es valido")
                except Exception as e:
                    st.error(f"Error: {str(e)}")

st.divider()
st.markdown(""
<div style="text-align: center; color: #666; font-size: 0.9rem;">
    Logica Subatomica - Probador de Teoremas | Version 1.0<br>
    Sistema de tableaux semanticos para logica con cuantificadores y operadores de termino
</div>
"", unsafe_allow_html=True)
