from app.runtime.strategy_discovery.graph_synthesis import HTNGraphSynthesizer
from app.runtime.strategy_discovery.graph_grammar import GraphGrammarEngine
from app.runtime.strategy_discovery.operator_generation import ConstrainedOperatorGenerator
from app.runtime.strategy_discovery.mutation import EvolutionaryGraphMutator
from app.runtime.strategy_discovery.evaluation import StrategyEvaluator
from app.runtime.strategy_discovery.repository import StrategyRepository


def test_htn_graph_synthesis():
    synthesizer = HTNGraphSynthesizer()
    dag = synthesizer.synthesize_dag(goal_intent="extract_financial_invoice")
    
    assert dag.dag_id != ""
    assert len(dag.nodes) >= 3
    assert dag.critical_path_ms > 0
    assert dag.total_estimated_cost_usd > 0


def test_graph_grammar_optimization():
    synthesizer = HTNGraphSynthesizer()
    grammar = GraphGrammarEngine()
    
    linear_dag = synthesizer.synthesize_dag(goal_intent="extract_financial_invoice")
    optimized_dag = grammar.rewrite_and_optimize(linear_dag)
    
    assert optimized_dag.parallelism_width >= 1
    assert optimized_dag.critical_path_ms <= linear_dag.critical_path_ms


def test_constrained_operator_generation():
    generator = ConstrainedOperatorGenerator()
    spec = generator.generate_operator("reconcile_tax_items", task_category="TABLE_RECONCILIATION")
    
    assert spec.is_ast_safe is True
    assert len(spec.safety_violations) == 0
    assert "def execute_reconcile_tax_items" in spec.generated_python_code


def test_evolutionary_mutation_and_evaluation():
    synthesizer = HTNGraphSynthesizer()
    mutator = EvolutionaryGraphMutator()
    evaluator = StrategyEvaluator()
    repo = StrategyRepository()
    
    base_dag = synthesizer.synthesize_dag()
    mutation_res = mutator.mutate_dag(base_dag, mutation_type="OPERATOR_SWAP")
    
    assert mutation_res.mutated_dag.dag_id != base_dag.dag_id
    
    eval_report = evaluator.evaluate_strategy(mutation_res.mutated_dag)
    assert 0.0 <= eval_report.novelty_score <= 1.0
    assert eval_report.expected_utility > 0
    
    rec = repo.register_strategy(mutation_res.mutated_dag, eval_report)
    assert rec.strategy_id == mutation_res.mutated_dag.dag_id
    assert len(repo.list_strategies()) == 1
