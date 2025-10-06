""")
    
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

tab1, tab2, tab3 = st.tabs(["🧪 Probar Fórmula", "📜 Probar Argumento", "📚 Ejemplos"])

with tab1:
    st.header("Probar Validez de una Fórmula")
    st.markdown("Ingresa una fórmula para verificar si es válida (tautología).")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        formula_input = st.text_input(
            "Fórmula:",
            value="A | -A",
            help="Escribe la fórmula usando la sintaxis de la guía"
        )
    
    with col2:
        prove_button = st.button("🔍 Probar", type="primary", use_container_width=True)
    
    show_steps = st.checkbox("Mostrar paso a paso", value=False)
    
    if prove_button and formula_input:
        try:
            parsed = parse(formula_input)
            
            st.markdown("### Fórmula Parseada")
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
                    '<div class="result-valid">✓ La fórmula es VÁLIDA (Tautología)</div>',
                    unsafe_allow_html=True
                )
            else:
                st.markdown(
                    '<div class="result-invalid">✗ La fórmula NO es válida</div>',
                    unsafe_allow_html=True
                )
            
            if show_steps and output:
                st.markdown("### Proceso del Tableau")
                with st.expander("Ver pasos detallados", expanded=True):
                    st.text(output)
        
        except ParseError as e:
            st.error(f"❌ Error al parsear la fórmula: {str(e)}")
            st.info("💡 Revisa la sintaxis en la guía de la barra lateral.")
        except Exception as e:
            st.error(f"❌ Error inesperado: {str(e)}")
            st.exception(e)

with tab2:
    st.header("Probar Validez de un Argumento")
    st.markdown("Ingresa premisas y conclusión para verificar si el argumento es válido.")
    
    st.markdown("#### Premisas")
    
    num_premises = st.number_input("Número de premisas:", min_value=1, max_value=10, value=2)
    
    premises_input = []
    for i in range(num_premises):
        default_val = "[A]B" if i == 0 else "[B]C" if i == 1 else ""
        premise = st.text_input(f"Premisa {i+1}:", key=f"premise_{i}", value=default_val)
        premises_input.append(premise)
    
    st.markdown("#### Conclusión")
    conclusion_input = st.text_input("Conclusión:", value="[A]C")
    
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
            
            st.markdown(f'**Conclusión:** <div class="formula-box">{parsed_conclusion}</div>', unsafe_allow_html=True)
            
            old_stdout = sys.stdout
            sys.stdout = captured_output = StringIO()
            
            prover = TableauProver(max_iterations=50)
            result = prover.prove_argument(parsed_premises, parsed_conclusion, verbose=show_steps_arg)
            
            sys.stdout = old_stdout
            output = captured_output.getvalue()
            
            st.markdown("### Resultado")
            
            if result:
                st.markdown(
                    '<div class="result-valid">✓ El argumento es VÁLIDO</div>',
                    unsafe_allow_html=True
                )
            else:
                st.markdown(
                    '<div class="result-invalid">✗ El argumento NO es válido</div>',
                    unsafe_allow_html=True
                )
            
            if show_steps_arg and output:
                st.markdown("### Proceso del Tableau")
                with st.expander("Ver pasos detallados", expanded=True):
                    st.text(output)
        
        except ParseError as e:
            st.error(f"❌ Error al parsear: {str(e)}")
            st.info("💡 Revisa la sintaxis en la guía.")
        except Exception as e:
            st.error(f"❌ Error inesperado: {str(e)}")
            st.exception(e)

with tab3:
    st.header("Ejemplos de Silogismos y Fórmulas")
    
    st.markdown("### Silogismos Clásicos")
    
    examples = {
        "Barbara": {
            "premises": ["[M]P", "[S]M"],
            "conclusion": "[S]P",
            "description": "Todo M es P, Todo S es M ⊢ Todo S es P"
        },
        "Celarent": {
            "premises": ["-<M>P", "[S]M"],
            "conclusion": "-<S>P",
            "description": "Ningún M es P, Todo S es M ⊢ Ningún S es P"
        },
        "Darii": {
            "premises": ["[M]P", "<S>M"],
            "conclusion": "<S>P",
            "description": "Todo M es P, Algún S es M ⊢ Algún S es P"
        },
        "Ferio": {
            "premises": ["-<M>P", "<S>M"],
            "conclusion": "<S>~P",
            "description": "Ningún M es P, Algún S es M ⊢ Algún S es no-P"
        },
    }
    
    for name, example in examples.items():
        with st.expander(f"**{name}** - {example['description']}"):
            st.markdown("**Premisas:**")
            for i, p in enumerate(example['premises'], 1):
                st.code(p, language=None)
            
            st.markdown("**Conclusión:**")
            st.code(example['conclusion'], language=None)
            
            if st.button(f"Probar {name}", key=f"example_{name}"):
                try:
                    parsed_premises = [parse(p) for p in example['premises']]
                    parsed_conclusion = parse(example['conclusion'])
                    
                    with st.spinner(f"Probando {name}..."):
                        prover = TableauProver(max_iterations=50)
                        result = prover.prove_argument(parsed_premises, parsed_conclusion, verbose=False)
                    
                    if result:
                        st.success(f"✓ {name} es VÁLIDO")
                    else:
                        st.warning(f"✗ {name} NO es válido en este sistema")
                except Exception as e:
                    st.error(f"Error: {str(e)}")
    
    st.divider()
    
    st.markdown("### Fórmulas Lógicas Clásicas")
    
    logic_examples = {
        "Ley del Tercero Excluido": "A | -A",
        "Ley de No Contradicción": "-(A & -A)",
        "Modus Ponens": "(A & (A -> B)) -> B",
        "Modus Tollens": "((A -> B) & -B) -> -A",
        "Silogismo Hipotético": "((A -> B) & (B -> C)) -> (A -> C)",
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
                        st.success(f"✓ {name} es VÁLIDO")
                    else:
                        st.warning(f"✗ {name} NO es válido")
                except Exception as e:
                    st.error(f"Error: {str(e)}")

st.divider()
st.markdown("""
<div style="text-align: center; color: #666; font-size: 0.9rem;">
    Lógica Subatómica - Probador de Teoremas | Versión 1.0<br>
    Sistema de tableaux semánticos para lógica con cuantificadores y operadores de término
</div>
""", unsafe_allow_html=True)
