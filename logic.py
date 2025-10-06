"""
Lógica Subatómica - Sistema de Representación de Fórmulas
Paso 1: Clases para términos y fórmulas
"""

# ============================================================================
# TÉRMINOS
# ============================================================================

class Term:
    """Clase base para términos"""
    pass

class AtomicTerm(Term):
    """Término atómico: A, B, C, etc."""
    def __init__(self, name):
        self.name = name
    
    def __str__(self):
        return self.name
    
    def __eq__(self, other):
        return isinstance(other, AtomicTerm) and self.name == other.name
    
    def __hash__(self):
        return hash(('atomic', self.name))

class Complement(Term):
    """Complemento de un término: Ā (no-A)"""
    def __init__(self, term):
        self.term = term
    
    def __str__(self):
        return f"{self.term}\u0304"  # Unicode combining overline
    
    def __eq__(self, other):
        return isinstance(other, Complement) and self.term == other.term
    
    def __hash__(self):
        return hash(('complement', self.term))

class Privation(Term):
    """Privación de un término: Â (in-A)"""
    def __init__(self, term):
        self.term = term
    
    def __str__(self):
        return f"{self.term}\u0302"  # Unicode combining circumflex
    
    def __eq__(self, other):
        return isinstance(other, Privation) and self.term == other.term
    
    def __hash__(self):
        return hash(('privation', self.term))


# ============================================================================
# FÓRMULAS
# ============================================================================

class Formula:
    """Clase base para fórmulas"""
    pass

class Existential(Formula):
    """Fórmula existencial: A (existe A)"""
    def __init__(self, term):
        self.term = term
    
    def __str__(self):
        return str(self.term)
    
    def __eq__(self, other):
        return isinstance(other, Existential) and self.term == other.term
    
    def __hash__(self):
        return hash(('existential', self.term))

class Universal(Formula):
    """Fórmula universal: [A]B (todo A es B)"""
    def __init__(self, subject, predicate):
        self.subject = subject
        self.predicate = predicate
    
    def __str__(self):
        return f"[{self.subject}]{self.predicate}"
    
    def __eq__(self, other):
        return (isinstance(other, Universal) and 
                self.subject == other.subject and 
                self.predicate == other.predicate)
    
    def __hash__(self):
        return hash(('universal', self.subject, self.predicate))

class Particular(Formula):
    """Fórmula particular: 《A》B (algún A es B)"""
    def __init__(self, subject, predicate):
        self.subject = subject
        self.predicate = predicate
    
    def __str__(self):
        return f"《{self.subject}》{self.predicate}"
    
    def __eq__(self, other):
        return (isinstance(other, Particular) and 
                self.subject == other.subject and 
                self.predicate == other.predicate)
    
    def __hash__(self):
        return hash(('particular', self.subject, self.predicate))

class Negation(Formula):
    """Negación: ¬φ"""
    def __init__(self, formula):
        self.formula = formula
    
    def __str__(self):
        return f"¬{self.formula}"
    
    def __eq__(self, other):
        return isinstance(other, Negation) and self.formula == other.formula
    
    def __hash__(self):
        return hash(('negation', self.formula))

class Conjunction(Formula):
    """Conjunción: φ ∧ ψ"""
    def __init__(self, left, right):
        self.left = left
        self.right = right
    
    def __str__(self):
        return f"({self.left} ∧ {self.right})"
    
    def __eq__(self, other):
        return (isinstance(other, Conjunction) and 
                self.left == other.left and self.right == other.right)
    
    def __hash__(self):
        return hash(('conjunction', self.left, self.right))

class Disjunction(Formula):
    """Disyunción: φ ∨ ψ"""
    def __init__(self, left, right):
        self.left = left
        self.right = right
    
    def __str__(self):
        return f"({self.left} ∨ {self.right})"
    
    def __eq__(self, other):
        return (isinstance(other, Disjunction) and 
                self.left == other.left and self.right == other.right)
    
    def __hash__(self):
        return hash(('disjunction', self.left, self.right))

class Conditional(Formula):
    """Condicional: φ → ψ"""
    def __init__(self, antecedent, consequent):
        self.antecedent = antecedent
        self.consequent = consequent
    
    def __str__(self):
        return f"({self.antecedent} → {self.consequent})"
    
    def __eq__(self, other):
        return (isinstance(other, Conditional) and 
                self.antecedent == other.antecedent and 
                self.consequent == other.consequent)
    
    def __hash__(self):
        return hash(('conditional', self.antecedent, self.consequent))

class Biconditional(Formula):
    """Bicondicional: φ ↔ ψ"""
    def __init__(self, left, right):
        self.left = left
        self.right = right
    
    def __str__(self):
        return f"({self.left} ↔ {self.right})"
    
    def __eq__(self, other):
        return (isinstance(other, Biconditional) and 
                self.left == other.left and self.right == other.right)
    
    def __hash__(self):
        return hash(('biconditional', self.left, self.right))


# ============================================================================
# EJEMPLOS DE USO
# ============================================================================

# ============================================================================
# PARSER
# ============================================================================

class ParseError(Exception):
    """Error durante el parsing"""
    pass

class Parser:
    """Parser para fórmulas de lógica subatómica
    
    Sintaxis:
        Términos:
            A, B, C, ...     - términos atómicos
            ~A               - complemento
            ^A               - privación
        
        Fórmulas:
            A                - existencial
            [A]B             - universal
            <A>B             - particular
            -φ               - negación
            φ & ψ            - conjunción
            φ | ψ            - disyunción
            φ -> ψ           - condicional
            φ <-> ψ          - bicondicional
            (φ)              - paréntesis
    """
    
    def __init__(self, text):
        self.text = text.replace(' ', '')  # Eliminar espacios
        self.pos = 0
    
    def peek(self, offset=0):
        """Mirar el carácter actual sin consumirlo"""
        pos = self.pos + offset
        if pos < len(self.text):
            return self.text[pos]
        return None
    
    def consume(self):
        """Consumir y retornar el carácter actual"""
        if self.pos < len(self.text):
            char = self.text[self.pos]
            self.pos += 1
            return char
        return None
    
    def expect(self, char):
        """Consumir un carácter esperado o lanzar error"""
        if self.peek() == char:
            return self.consume()
        raise ParseError(f"Expected '{char}' at position {self.pos}, got '{self.peek()}'")
    
    def parse_term(self):
        """Parsear un término"""
        # Complemento: ~A
        if self.peek() == '~':
            self.consume()
            inner = self.parse_term()
            return Complement(inner)
        
        # Privación: ^A
        if self.peek() == '^':
            self.consume()
            inner = self.parse_term()
            return Privation(inner)
        
        # Término atómico: letra mayúscula
        char = self.peek()
        if char and char.isupper():
            self.consume()
            return AtomicTerm(char)
        
        raise ParseError(f"Expected term at position {self.pos}")
    
    def parse_primary(self):
        """Parsear fórmula primaria (atómica, categorial, o entre paréntesis)"""
        # Negación: -φ
        if self.peek() == '-':
            self.consume()
            formula = self.parse_primary()
            return Negation(formula)
        
        # Paréntesis: (φ)
        if self.peek() == '(':
            self.consume()
            formula = self.parse_biconditional()
            self.expect(')')
            return formula
        
        # Universal: [A]B
        if self.peek() == '[':
            self.consume()
            subject = self.parse_term()
            self.expect(']')
            predicate = self.parse_term()
            return Universal(subject, predicate)
        
        # Particular: <A>B
        if self.peek() == '<':
            self.consume()
            subject = self.parse_term()
            self.expect('>')
            predicate = self.parse_term()
            return Particular(subject, predicate)
        
        # Existencial o término simple: A
        if self.peek() and self.peek().isupper():
            term = self.parse_term()
            return Existential(term)
        
        raise ParseError(f"Unexpected character at position {self.pos}: '{self.peek()}'")
    
    def parse_conjunction(self):
        """Parsear conjunción: φ & ψ"""
        left = self.parse_primary()
        
        while self.peek() == '&':
            self.consume()
            right = self.parse_primary()
            left = Conjunction(left, right)
        
        return left
    
    def parse_disjunction(self):
        """Parsear disyunción: φ | ψ"""
        left = self.parse_conjunction()
        
        while self.peek() == '|':
            self.consume()
            right = self.parse_conjunction()
            left = Disjunction(left, right)
        
        return left
    
    def parse_conditional(self):
        """Parsear condicional: φ -> ψ"""
        left = self.parse_disjunction()
        
        if self.peek() == '-' and self.peek(1) == '>':
            self.consume()  # -
            self.consume()  # >
            right = self.parse_conditional()
            return Conditional(left, right)
        
        return left
    
    def parse_biconditional(self):
        """Parsear bicondicional: φ <-> ψ"""
        left = self.parse_conditional()
        
        if self.peek() == '<' and self.peek(1) == '-' and self.peek(2) == '>':
            self.consume()  # <
            self.consume()  # -
            self.consume()  # >
            right = self.parse_biconditional()
            return Biconditional(left, right)
        
        return left
    
    def parse(self):
        """Parsear una fórmula completa"""
        formula = self.parse_biconditional()
        
        if self.pos < len(self.text):
            raise ParseError(f"Unexpected characters after formula: '{self.text[self.pos:]}'")
        
        return formula


def parse(text):
    """Función auxiliar para parsear fórmulas"""
    return Parser(text).parse()


# ============================================================================
# ESTRUCTURA DEL TABLEAU
# ============================================================================

class LabeledFormula:
    """Fórmula etiquetada con un estado: (φ, x)"""
    def __init__(self, formula, state):
        self.formula = formula
        self.state = state
    
    def __str__(self):
        return f"{self.formula}, {self.state}"
    
    def __eq__(self, other):
        return (isinstance(other, LabeledFormula) and 
                self.formula == other.formula and 
                self.state == other.state)
    
    def __hash__(self):
        return hash((self.formula, self.state))


class Relation:
    """Clase base para relaciones entre estados"""
    pass


class RelationQ(Relation):
    """Relación ternaria: Qxyz"""
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
    
    def __str__(self):
        return f"Q{self.x}{self.y}{self.z}"
    
    def __eq__(self, other):
        return (isinstance(other, RelationQ) and 
                self.x == other.x and self.y == other.y and self.z == other.z)
    
    def __hash__(self):
        return hash(('Q', self.x, self.y, self.z))


class RelationS(Relation):
    """Relación binaria: Sxy (para complemento y privación)"""
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __str__(self):
        return f"S{self.x}{self.y}"
    
    def __eq__(self, other):
        return (isinstance(other, RelationS) and 
                self.x == other.x and self.y == other.y)
    
    def __hash__(self):
        return hash(('S', self.x, self.y))


class Branch:
    """Una rama del tableau"""
    def __init__(self, parent=None):
        self.formulas = []      # Lista de LabeledFormula
        self.relations = []     # Lista de Relation (Q o S)
        self.closed = False
        self.parent = parent    # Rama padre (para heredar información)
    
    def add_formula(self, formula, state):
        """Agregar una fórmula etiquetada"""
        lf = LabeledFormula(formula, state)
        self.formulas.append(lf)
        return lf
    
    def add_relation(self, relation):
        """Agregar una relación"""
        self.relations.append(relation)
        return relation
    
    def get_all_formulas(self):
        """Obtener todas las fórmulas (incluyendo las heredadas del padre)"""
        if self.parent:
            return self.parent.get_all_formulas() + self.formulas
        return self.formulas[:]
    
    def get_all_relations(self):
        """Obtener todas las relaciones (incluyendo las heredadas del padre)"""
        if self.parent:
            return self.parent.get_all_relations() + self.relations
        return self.relations[:]
    
    def check_closure(self):
        """Verificar si la rama está cerrada (contiene A,x y ¬A,x)"""
        all_formulas = self.get_all_formulas()
        
        for i, lf1 in enumerate(all_formulas):
            for lf2 in all_formulas[i+1:]:
                # Mismo estado
                if lf1.state == lf2.state:
                    # Una es negación de la otra
                    if isinstance(lf1.formula, Negation):
                        if lf1.formula.formula == lf2.formula:
                            self.closed = True
                            return True
                    elif isinstance(lf2.formula, Negation):
                        if lf2.formula.formula == lf1.formula:
                            self.closed = True
                            return True
        
        return False
    
    def __str__(self):
        """Representación en texto de la rama"""
        lines = []
        for lf in self.formulas:
            lines.append(str(lf))
        for rel in self.relations:
            lines.append(str(rel))
        if self.closed:
            lines.append("✗ CERRADA")
        return "\n".join(lines)


class Tableau:
    """El tableau completo - árbol de ramas"""
    def __init__(self, initial_formulas):
        """
        Inicializar tableau con fórmulas iniciales
        initial_formulas: lista de tuplas (formula, state)
        """
        self.root = Branch()
        self.branches = [self.root]  # Lista de ramas abiertas
        
        # Agregar fórmulas iniciales
        for formula, state in initial_formulas:
            self.root.add_formula(formula, state)
        
        # Generador de variables frescas
        self.var_counter = 0
    
    def fresh_var(self):
        """Generar una variable fresca para estados"""
        # Ciclo: x, y, z, x1, y1, z1, x2, y2, z2, ...
        base_vars = ['x', 'y', 'z']
        if self.var_counter < 3:
            var = base_vars[self.var_counter]
        else:
            idx = self.var_counter - 3
            var = base_vars[idx % 3] + str(idx // 3 + 1)
        self.var_counter += 1
        return var
    
    def split_branch(self, branch, left_items, right_items):
        """
        Dividir una rama en dos
        left_items, right_items: listas de (formula, state) o relation
        """
        # Crear dos nuevas ramas hijas
        left_branch = Branch(parent=branch)
        right_branch = Branch(parent=branch)
        
        # Agregar items a cada rama
        for item in left_items:
            if isinstance(item, tuple):  # (formula, state)
                left_branch.add_formula(item[0], item[1])
            else:  # Relation
                left_branch.add_relation(item)
        
        for item in right_items:
            if isinstance(item, tuple):
                right_branch.add_formula(item[0], item[1])
            else:
                right_branch.add_relation(item)
        
        # Remover rama original y agregar las nuevas
        self.branches.remove(branch)
        self.branches.append(left_branch)
        self.branches.append(right_branch)
        
        return left_branch, right_branch
    
    def is_closed(self):
        """Verificar si el tableau está cerrado (todas las ramas cerradas)"""
        for branch in self.branches:
            branch.check_closure()
            if not branch.closed:
                return False
        return True
    
    def __str__(self):
        """Representación en texto del tableau"""
        if len(self.branches) == 1:
            return str(self.branches[0])
        
        result = ["=== TABLEAU CON MÚLTIPLES RAMAS ===\n"]
        for i, branch in enumerate(self.branches):
            result.append(f"--- Rama {i+1} ---")
            result.append(str(branch))
            result.append("")
        return "\n".join(result)


# ============================================================================
# EJEMPLOS DE USO
# ============================================================================

if __name__ == "__main__":
    print("=== PARSER DE LÓGICA SUBATÓMICA ===\n")
    
    # Ejemplos de fórmulas
    examples = [
        "A",                          # Existencial
        "[A]B",                       # Universal
        "<A>B",                       # Particular
        "-[A]B",                      # Negación de universal
        "[~A]B",                      # Todo no-A es B
        "[A]^B",                      # Todo A es in-B
        "[~A]^B",                     # Todo no-A es in-B
        "([A]B & [B]C) -> [A]C",     # Barbara
        "-<A>B",                      # Ningún A es B
        "A | B",                      # A o B
        "(A & B) -> C",               # Si A y B entonces C
        "[A]B <-> [B]A",              # Todo A es B sii todo B es A
    ]
    
    for expr in examples:
        try:
            formula = parse(expr)
            print(f"Input:  {expr}")
            print(f"Parsed: {formula}")
            print()
        except ParseError as e:
            print(f"Error parsing '{expr}': {e}")
            print()
    
    print("\n=== ESTRUCTURA DE TABLEAU ===\n")
    
    # Ejemplo simple: crear un tableau con algunas fórmulas
    A = AtomicTerm('A')
    B = AtomicTerm('B')
    
    # [A]B, w
    formula1 = Universal(A, B)
    
    # A, w
    formula2 = Existential(A)
    
    # Crear tableau
    tableau = Tableau([
        (formula1, 'w'),
        (formula2, 'w')
    ])
    
    print("Tableau inicial:")
    print(tableau)
    print()
    
    # Agregar una relación Q
    branch = tableau.branches[0]
    branch.add_relation(RelationQ('w', 'x', 'y'))
    
    print("Después de agregar Qwxy:")
    print(tableau)
    print()
    
    # Dividir la rama
    neg_A = Negation(Existential(A))
    tableau.split_branch(
        branch,
        left_items=[(neg_A, 'x')],
        right_items=[(Existential(B), 'y')]
    )
    
    print("Después de dividir:")
    print(tableau)
    print()
    
    # Verificar cierre
    print(f"¿Tableau cerrado? {tableau.is_closed()}")


# ============================================================================
# MOTOR DE REGLAS
# ============================================================================

class Rule:
    """Clase base para reglas de tableau"""
    
    def applies_to(self, labeled_formula, branch):
        """
        Verificar si la regla aplica a una fórmula etiquetada en una rama
        Retorna True si aplica, False si no
        """
        raise NotImplementedError
    
    def apply(self, labeled_formula, branch, tableau):
        """
        Aplicar la regla a una fórmula en una rama
        Retorna True si se aplicó exitosamente
        """
        raise NotImplementedError
    
    def __str__(self):
        return self.__class__.__name__


# ============================================================================
# REGLAS DE CUANTIFICADORES
# ============================================================================

class UniversalAffirmativeRule(Rule):
    """
    Regla para [A]B, x
    Requiere Qxyz en el tableau
    Ramifica: ¬A, y | B, z
    """
    
    def applies_to(self, labeled_formula, branch):
        formula = labeled_formula.formula
        # Debe ser una Universal
        if not isinstance(formula, Universal):
            return False
        
        # Debe existir alguna relación Qxyz donde x = estado de la fórmula
        state = labeled_formula.state
        relations = branch.get_all_relations()
        
        for rel in relations:
            if isinstance(rel, RelationQ) and rel.x == state:
                return True
        
        return False
    
    def apply(self, labeled_formula, branch, tableau):
        formula = labeled_formula.formula
        state = labeled_formula.state
        
        # Buscar todas las relaciones Qxyz con x = state
        relations = branch.get_all_relations()
        applied = False
        
        for rel in relations:
            if isinstance(rel, RelationQ) and rel.x == state:
                # Ramificar: ¬A, y | B, z
                subject = formula.subject
                predicate = formula.predicate
                
                left_items = [(Negation(Existential(subject)), rel.y)]
                right_items = [(Existential(predicate), rel.z)]
                
                tableau.split_branch(branch, left_items, right_items)
                applied = True
                break  # Solo aplicamos una vez por ahora
        
        return applied


class UniversalNegativeRule(Rule):
    """
    Regla para ¬《A》B, x
    Requiere Qxyz en el tableau
    Ramifica: ¬A, y | ¬B, z
    """
    
    def applies_to(self, labeled_formula, branch):
        formula = labeled_formula.formula
        
        # Debe ser negación de Particular
        if not isinstance(formula, Negation):
            return False
        if not isinstance(formula.formula, Particular):
            return False
        
        # Debe existir Qxyz con x = estado
        state = labeled_formula.state
        relations = branch.get_all_relations()
        
        for rel in relations:
            if isinstance(rel, RelationQ) and rel.x == state:
                return True
        
        return False
    
    def apply(self, labeled_formula, branch, tableau):
        neg_particular = labeled_formula.formula.formula  # La Particular dentro de la Negation
        state = labeled_formula.state
        
        relations = branch.get_all_relations()
        applied = False
        
        for rel in relations:
            if isinstance(rel, RelationQ) and rel.x == state:
                # Ramificar: ¬A, y | ¬B, z
                subject = neg_particular.subject
                predicate = neg_particular.predicate
                
                left_items = [(Negation(Existential(subject)), rel.y)]
                right_items = [(Negation(Existential(predicate)), rel.z)]
                
                tableau.split_branch(branch, left_items, right_items)
                applied = True
                break
        
        return applied


class ParticularAffirmativeRule(Rule):
    """
    Regla para 《A》B, x
    Crea nueva relación Qxyz (variables frescas)
    Agrega: A, y y B, z
    """
    
    def applies_to(self, labeled_formula, branch):
        formula = labeled_formula.formula
        return isinstance(formula, Particular)
    
    def apply(self, labeled_formula, branch, tableau):
        formula = labeled_formula.formula
        state = labeled_formula.state
        
        # Crear variables frescas
        y = tableau.fresh_var()
        z = tableau.fresh_var()
        
        # Crear nueva relación Q
        new_q = RelationQ(state, y, z)
        branch.add_relation(new_q)
        
        # Agregar fórmulas
        subject = formula.subject
        predicate = formula.predicate
        
        branch.add_formula(Existential(subject), y)
        branch.add_formula(Existential(predicate), z)
        
        return True


class ParticularNegativeRule(Rule):
    """
    Regla para ¬[A]B, x
    Crea nueva relación Qxyz (variables frescas)
    Agrega: A, y y ¬B, z
    """
    
    def applies_to(self, labeled_formula, branch):
        formula = labeled_formula.formula
        
        # Debe ser negación de Universal
        if not isinstance(formula, Negation):
            return False
        return isinstance(formula.formula, Universal)
    
    def apply(self, labeled_formula, branch, tableau):
        universal = labeled_formula.formula.formula  # La Universal dentro de la Negation
        state = labeled_formula.state
        
        # Crear variables frescas
        y = tableau.fresh_var()
        z = tableau.fresh_var()
        
        # Crear nueva relación Q
        new_q = RelationQ(state, y, z)
        branch.add_relation(new_q)
        
        # Agregar fórmulas
        subject = universal.subject
        predicate = universal.predicate
        
        branch.add_formula(Existential(subject), y)
        branch.add_formula(Negation(Existential(predicate)), z)
        
        return True


# ============================================================================
# REGLAS DE OPERADORES DE TÉRMINO
# ============================================================================

class ComplementAffirmativeRule(Rule):
    """
    Regla para Ā, x
    Requiere Sxy en el tableau
    Agrega: ¬A, y
    """
    
    def applies_to(self, labeled_formula, branch):
        formula = labeled_formula.formula
        
        # Debe ser existencial de un complemento
        if not isinstance(formula, Existential):
            return False
        if not isinstance(formula.term, Complement):
            return False
        
        # Debe existir Sxy con x = estado
        state = labeled_formula.state
        relations = branch.get_all_relations()
        
        for rel in relations:
            if isinstance(rel, RelationS) and rel.x == state:
                return True
        
        return False
    
    def apply(self, labeled_formula, branch, tableau):
        complement_term = labeled_formula.formula.term
        inner_term = complement_term.term
        state = labeled_formula.state
        
        relations = branch.get_all_relations()
        applied = False
        
        for rel in relations:
            if isinstance(rel, RelationS) and rel.x == state:
                # Agregar ¬A, y
                branch.add_formula(Negation(Existential(inner_term)), rel.y)
                applied = True
                break
        
        return applied


class ComplementNegativeRule(Rule):
    """
    Regla para ¬Ā, x
    Crea nueva relación Sxy (variable fresca)
    Agrega: A, y
    """
    
    def applies_to(self, labeled_formula, branch):
        formula = labeled_formula.formula
        
        # Debe ser negación de existencial de complemento
        if not isinstance(formula, Negation):
            return False
        if not isinstance(formula.formula, Existential):
            return False
        if not isinstance(formula.formula.term, Complement):
            return False
        
        return True
    
    def apply(self, labeled_formula, branch, tableau):
        complement_term = labeled_formula.formula.formula.term
        inner_term = complement_term.term
        state = labeled_formula.state
        
        # Crear variable fresca
        y = tableau.fresh_var()
        
        # Crear nueva relación S
        new_s = RelationS(state, y)
        branch.add_relation(new_s)
        
        # Agregar A, y
        branch.add_formula(Existential(inner_term), y)
        
        return True


class PrivationAffirmativeRule(Rule):
    """
    Regla para Â, x
    Requiere Sxy en el tableau
    Agrega: ¬A, y
    """
    
    def applies_to(self, labeled_formula, branch):
        formula = labeled_formula.formula
        
        # Debe ser existencial de una privación
        if not isinstance(formula, Existential):
            return False
        if not isinstance(formula.term, Privation):
            return False
        
        # Debe existir Sxy con x = estado
        state = labeled_formula.state
        relations = branch.get_all_relations()
        
        for rel in relations:
            if isinstance(rel, RelationS) and rel.x == state:
                return True
        
        return False
    
    def apply(self, labeled_formula, branch, tableau):
        privation_term = labeled_formula.formula.term
        inner_term = privation_term.term
        state = labeled_formula.state
        
        relations = branch.get_all_relations()
        applied = False
        
        for rel in relations:
            if isinstance(rel, RelationS) and rel.x == state:
                # Agregar ¬A, y
                branch.add_formula(Negation(Existential(inner_term)), rel.y)
                applied = True
                break
        
        return applied


class PrivationNegativeRule(Rule):
    """
    Regla para ¬Â, x
    Crea nueva relación Sxy (variable fresca)
    Agrega: A, y
    """
    
    def applies_to(self, labeled_formula, branch):
        formula = labeled_formula.formula
        
        # Debe ser negación de existencial de privación
        if not isinstance(formula, Negation):
            return False
        if not isinstance(formula.formula, Existential):
            return False
        if not isinstance(formula.formula.term, Privation):
            return False
        
        return True
    
    def apply(self, labeled_formula, branch, tableau):
        privation_term = labeled_formula.formula.formula.term
        inner_term = privation_term.term
        state = labeled_formula.state
        
        # Crear variable fresca
        y = tableau.fresh_var()
        
        # Crear nueva relación S
        new_s = RelationS(state, y)
        branch.add_relation(new_s)
        
        # Agregar A, y
        branch.add_formula(Existential(inner_term), y)
        
        return True


# ============================================================================
# LISTA DE TODAS LAS REGLAS
# ============================================================================

ALL_RULES = [
    # Cuantificadores
    ParticularAffirmativeRule(),
    ParticularNegativeRule(),
    UniversalAffirmativeRule(),
    UniversalNegativeRule(),
    # Operadores de término
    ComplementNegativeRule(),
    ComplementAffirmativeRule(),
    PrivationNegativeRule(),
    PrivationAffirmativeRule(),
]


# ============================================================================
# REGLAS DE CONECTIVOS CLÁSICOS
# ============================================================================

class ConjunctionRule(Rule):
    """
    Regla para φ ∧ ψ, x
    Agrega (tronco): φ, x y ψ, x
    """
    
    def applies_to(self, labeled_formula, branch):
        return isinstance(labeled_formula.formula, Conjunction)
    
    def apply(self, labeled_formula, branch, tableau):
        formula = labeled_formula.formula
        state = labeled_formula.state
        
        # Agregar ambas fórmulas al tronco
        branch.add_formula(formula.left, state)
        branch.add_formula(formula.right, state)
        
        return True


class DisjunctionRule(Rule):
    """
    Regla para φ ∨ ψ, x
    Ramifica: φ, x | ψ, x
    """
    
    def applies_to(self, labeled_formula, branch):
        return isinstance(labeled_formula.formula, Disjunction)
    
    def apply(self, labeled_formula, branch, tableau):
        formula = labeled_formula.formula
        state = labeled_formula.state
        
        # Ramificar
        left_items = [(formula.left, state)]
        right_items = [(formula.right, state)]
        
        tableau.split_branch(branch, left_items, right_items)
        
        return True


class ConditionalRule(Rule):
    """
    Regla para φ → ψ, x
    Ramifica: ¬φ, x | ψ, x
    """
    
    def applies_to(self, labeled_formula, branch):
        return isinstance(labeled_formula.formula, Conditional)
    
    def apply(self, labeled_formula, branch, tableau):
        formula = labeled_formula.formula
        state = labeled_formula.state
        
        # Ramificar
        left_items = [(Negation(formula.antecedent), state)]
        right_items = [(formula.consequent, state)]
        
        tableau.split_branch(branch, left_items, right_items)
        
        return True


class BiconditionalRule(Rule):
    """
    Regla para φ ↔ ψ, x
    Ramifica: (φ, x y ψ, x) | (¬φ, x y ¬ψ, x)
    """
    
    def applies_to(self, labeled_formula, branch):
        return isinstance(labeled_formula.formula, Biconditional)
    
    def apply(self, labeled_formula, branch, tableau):
        formula = labeled_formula.formula
        state = labeled_formula.state
        
        # Ramificar en dos
        left_items = [
            (formula.left, state),
            (formula.right, state)
        ]
        right_items = [
            (Negation(formula.left), state),
            (Negation(formula.right), state)
        ]
        
        tableau.split_branch(branch, left_items, right_items)
        
        return True


class DoubleNegationRule(Rule):
    """
    Regla para ¬¬φ, x
    Agrega (tronco): φ, x
    """
    
    def applies_to(self, labeled_formula, branch):
        formula = labeled_formula.formula
        
        # Debe ser negación de negación
        if not isinstance(formula, Negation):
            return False
        return isinstance(formula.formula, Negation)
    
    def apply(self, labeled_formula, branch, tableau):
        inner_formula = labeled_formula.formula.formula.formula
        state = labeled_formula.state
        
        # Agregar la fórmula sin las dos negaciones
        branch.add_formula(inner_formula, state)
        
        return True


class NegatedConjunctionRule(Rule):
    """
    Regla para ¬(φ ∧ ψ), x
    Ramifica: ¬φ, x | ¬ψ, x
    """
    
    def applies_to(self, labeled_formula, branch):
        formula = labeled_formula.formula
        
        if not isinstance(formula, Negation):
            return False
        return isinstance(formula.formula, Conjunction)
    
    def apply(self, labeled_formula, branch, tableau):
        conjunction = labeled_formula.formula.formula
        state = labeled_formula.state
        
        # Ramificar
        left_items = [(Negation(conjunction.left), state)]
        right_items = [(Negation(conjunction.right), state)]
        
        tableau.split_branch(branch, left_items, right_items)
        
        return True


class NegatedDisjunctionRule(Rule):
    """
    Regla para ¬(φ ∨ ψ), x
    Agrega (tronco): ¬φ, x y ¬ψ, x
    """
    
    def applies_to(self, labeled_formula, branch):
        formula = labeled_formula.formula
        
        if not isinstance(formula, Negation):
            return False
        return isinstance(formula.formula, Disjunction)
    
    def apply(self, labeled_formula, branch, tableau):
        disjunction = labeled_formula.formula.formula
        state = labeled_formula.state
        
        # Agregar ambas negaciones al tronco
        branch.add_formula(Negation(disjunction.left), state)
        branch.add_formula(Negation(disjunction.right), state)
        
        return True


class NegatedConditionalRule(Rule):
    """
    Regla para ¬(φ → ψ), x
    Agrega (tronco): φ, x y ¬ψ, x
    """
    
    def applies_to(self, labeled_formula, branch):
        formula = labeled_formula.formula
        
        if not isinstance(formula, Negation):
            return False
        return isinstance(formula.formula, Conditional)
    
    def apply(self, labeled_formula, branch, tableau):
        conditional = labeled_formula.formula.formula
        state = labeled_formula.state
        
        # Agregar ambas al tronco
        branch.add_formula(conditional.antecedent, state)
        branch.add_formula(Negation(conditional.consequent), state)
        
        return True


class NegatedBiconditionalRule(Rule):
    """
    Regla para ¬(φ ↔ ψ), x
    Ramifica: (φ, x y ¬ψ, x) | (¬φ, x y ψ, x)
    """
    
    def applies_to(self, labeled_formula, branch):
        formula = labeled_formula.formula
        
        if not isinstance(formula, Negation):
            return False
        return isinstance(formula.formula, Biconditional)
    
    def apply(self, labeled_formula, branch, tableau):
        biconditional = labeled_formula.formula.formula
        state = labeled_formula.state
        
        # Ramificar
        left_items = [
            (biconditional.left, state),
            (Negation(biconditional.right), state)
        ]
        right_items = [
            (Negation(biconditional.left), state),
            (biconditional.right, state)
        ]
        
        tableau.split_branch(branch, left_items, right_items)
        
        return True


# ============================================================================
# LISTA COMPLETA DE TODAS LAS REGLAS
# ============================================================================

ALL_RULES = [
    # Cuantificadores (crear Q primero, luego usar)
    ParticularAffirmativeRule(),
    ParticularNegativeRule(),
    UniversalAffirmativeRule(),
    UniversalNegativeRule(),
    # Operadores de término (crear S primero, luego usar)
    ComplementNegativeRule(),
    ComplementAffirmativeRule(),
    PrivationNegativeRule(),
    PrivationAffirmativeRule(),
    # Conectivos - reglas de tronco primero (más eficientes)
    ConjunctionRule(),
    NegatedDisjunctionRule(),
    NegatedConditionalRule(),
    DoubleNegationRule(),
    # Conectivos - reglas de ramificación
    DisjunctionRule(),
    ConditionalRule(),
    BiconditionalRule(),
    NegatedConjunctionRule(),
    NegatedBiconditionalRule(),
]


# ============================================================================
# MOTOR DE APLICACIÓN AUTOMÁTICA
# ============================================================================

class TableauProver:
    """Motor que aplica reglas automáticamente para probar fórmulas"""
    
    def __init__(self, rules=None, max_iterations=100):
        self.rules = rules if rules else ALL_RULES
        self.max_iterations = max_iterations
        self.applied_rules = []  # Historia de reglas aplicadas
    
    def prove(self, formula, initial_state='w', verbose=False):
        """
        Intentar probar una fórmula
        Retorna True si es válida (tableau cierra), False si no
        """
        # Crear tableau con la negación de la fórmula
        negated = Negation(formula)
        tableau = Tableau([(negated, initial_state)])
        
        if verbose:
            print("=== INTENTO DE PRUEBA ===")
            print(f"Fórmula a probar: {formula}")
            print(f"Negación: {negated}\n")
            print("Tableau inicial:")
            print(tableau)
            print("\n" + "="*50 + "\n")
        
        # Aplicar reglas iterativamente
        iteration = 0
        while iteration < self.max_iterations:
            iteration += 1
            
            if verbose:
                print(f"--- Iteración {iteration} ---")
            
            # Intentar aplicar reglas a todas las ramas abiertas
            applied_any = False
            
            # Trabajar con copia de branches porque pueden modificarse
            current_branches = tableau.branches[:]
            
            for branch in current_branches:
                if branch.closed:
                    continue
                
                # Verificar cierre antes de aplicar reglas
                if branch.check_closure():
                    if verbose:
                        print(f"Rama cerrada por contradicción")
                    continue
                
                # Intentar aplicar cada regla a cada fórmula
                formulas = branch.get_all_formulas()
                
                for lf in formulas:
                    for rule in self.rules:
                        if rule.applies_to(lf, branch):
                            if verbose:
                                print(f"Aplicando {rule} a: {lf}")
                            
                            # Aplicar la regla
                            success = rule.apply(lf, branch, tableau)
                            
                            if success:
                                self.applied_rules.append((rule, lf))
                                applied_any = True
                                
                                if verbose:
                                    print(f"Resultado:\n{tableau}\n")
                                
                                # Después de aplicar una regla, salir
                                # para recalcular las ramas
                                break
                    
                    if applied_any:
                        break
                
                if applied_any:
                    break
            
            # Si no se aplicó ninguna regla, terminar
            if not applied_any:
                if verbose:
                    print("No hay más reglas aplicables")
                break
            
            # Verificar si el tableau está cerrado
            if tableau.is_closed():
                if verbose:
                    print("\n" + "="*50)
                    print("¡TABLEAU CERRADO! La fórmula es VÁLIDA")
                    print("="*50)
                return True
        
        # Si llegamos aquí, el tableau no cerró
        if verbose:
            print("\n" + "="*50)
            print("Tableau NO cerrado. La fórmula NO es válida")
            print("="*50)
            print("\nTableau final:")
            print(tableau)
        
        return False
    
    def prove_argument(self, premises, conclusion, verbose=False):
        """
        Probar un argumento: premises ⊢ conclusion
        Construye (premises[0] ∧ premises[1] ∧ ... ∧ premises[n]) → conclusion
        """
        if not premises:
            return self.prove(conclusion, verbose=verbose)
        
        # Construir conjunción de premisas
        conj = premises[0]
        for premise in premises[1:]:
            conj = Conjunction(conj, premise)
        
        # Construir condicional
        argument = Conditional(conj, conclusion)
        
        if verbose:
            print("=== PRUEBA DE ARGUMENTO ===")
            print("Premisas:")
            for i, p in enumerate(premises, 1):
                print(f"  {i}. {p}")
            print(f"Conclusión: {conclusion}\n")
        
        return self.prove(argument, verbose=verbose)


# ============================================================================
# EJEMPLOS Y PRUEBAS
# ============================================================================

def test_barbara():
    """Probar el silogismo Barbara"""
    print("="*60)
    print("PRUEBA: SILOGISMO BARBARA")
    print("="*60)
    
    # [A]B, [B]C ⊢ [A]C
    A = AtomicTerm('A')
    B = AtomicTerm('B')
    C = AtomicTerm('C')
    
    premise1 = Universal(A, B)  # Todo A es B
    premise2 = Universal(B, C)  # Todo B es C
    conclusion = Universal(A, C)  # Todo A es C
    
    prover = TableauProver()
    result = prover.prove_argument([premise1, premise2], conclusion, verbose=True)
    
    print(f"\n✓ Barbara es {'VÁLIDO' if result else 'INVÁLIDO'}")
    return result


def test_simple_particular():
    """Probar una fórmula particular simple"""
    print("\n" + "="*60)
    print("PRUEBA: FÓRMULA PARTICULAR SIMPLE")
    print("="*60)
    
    # <A>B
    A = AtomicTerm('A')
    B = AtomicTerm('B')
    
    formula = Particular(A, B)
    
    prover = TableauProver()
    result = prover.prove(formula, verbose=True)
    
    print(f"\n✓ <A>B es {'VÁLIDO' if result else 'INVÁLIDO'}")
    return result


def test_law_of_excluded_middle():
    """Probar la ley del tercero excluido: A ∨ ¬A"""
    print("\n" + "="*60)
    print("PRUEBA: LEY DEL TERCERO EXCLUIDO")
    print("="*60)
    
    A = AtomicTerm('A')
    formula = Disjunction(Existential(A), Negation(Existential(A)))
    
    prover = TableauProver()
    result = prover.prove(formula, verbose=True)
    
    print(f"\n✓ A ∨ ¬A es {'VÁLIDO' if result else 'INVÁLIDO'}")
    return result


if __name__ == "__main__":
    # Ejecutar pruebas solo si se ejecuta directamente
    print("Ejecutando pruebas del sistema...\n")
    test_barbara()
    test_simple_particular()
    test_law_of_excluded_middle()
    
    print("\n" + "="*60)
    print("Sistema listo. Para usar la interfaz web, ejecuta:")
    print("  streamlit run app.py")
    print("="*60)
