MODULE_1_PLAN = {
    "module": {
        "name": "Module 1 – Core Vocabulary Training",
        "mode": "adaptive_human_guided",
        "input": {
            "the_new_word": "string",
            "practice_list": [
                "string"
            ],
            "practice_level": "A1 | A2 | B1 | B2 | C1",
            "strict_json_required": True
        },
        "practice_level_constraints": {
            "instruction": "Before generating any explanation, task, exercise, or feedback, internally compare complexity against the defined practice_level. Allow slight vocabulary stretch (up to half level above), but grammar structures must remain at the base practice_level. If complexity exceeds allowed tolerance, simplify it. Never exceed one full CEFR level above practice_level.",  # noqa: E501
            "affects": [
                "explanation_complexity",
                "sentence_length",
                "grammar_structures",
                "vocabulary_choice",
                "tense_selection",
                "feedback_language"
            ],
            "level_control": {
                "mode": "growth",
                "allow_slight_vocabulary_stretch": True,
                "max_vocabulary_exceed": 0.5,
                "no_grammar_above_base_level": True,
                "allow_minor_structure_variation": True,
                "never_exceed_next_full_level": True,
                "simplify_if_uncertain": True,
                "internal_level_check_required": True,
                "conceptual_abstraction_must_match_base_level": True
            },
            "difficulty_distribution_model": {
                "base_level_numeric": {
                    "A1": 1.0,
                    "A2": 2.0,
                    "B1": 3.0,
                    "B2": 4.0,
                    "C1": 5.0
                },
                "min_review_depth_levels": 1,
                "max_forward_stretch_levels": 1.1,
                "preferred_center_offset_min": 0.5,
                "preferred_center_offset_max": 0.9,
                "distribution_bias": "upper_band",
                "stretch_probability": 0.1
            }
        },
        "goal": {
            "learn_new_word": True,
            "reinforce_practice_list": True,
            "adaptive_difficulty": True,
            "gpt_recommends_next_step": True,
            "user_controls_progression": True
        },
        "session_flow": {
            "phase_1_new_word": {
                "task": "explain_word",
                "json_only": True,
                "rules": {
                    "examples_min": 2,
                    "examples_max": 5,
                    "respect_practice_level": True,
                    "complete_forms_required": True,
                    "no_extra_keys": True,
                    "no_missing_keys": True
                },
                "response_schema": {
                    "mode": "explanation",
                    "word": "string",
                    "partOfSpeech": "string",
                    "pronunciation": "string",
                    "definition": "string",
                    "meaning": "string",
                    "examples": [
                        {
                            "de": "string",
                            "en": "string"
                        }
                    ],
                    "forms": {
                        "praesens": "string",
                        "praeteritum": "string",
                        "perfekt": "string"
                    }
                }
            },
            "phase_2_exercises": {
                "json_only": True,
                "sequential_mode": True,
                "exercise_progression": "one_per_message",
                "exact_exercise_count": 5,
                "tasks_per_exercise": 5,
                "exact_task_count": 5,
                "rules": {
                    "focus_primary": "the_new_word",
                    "reinforce": "practice_list",
                    "allow_additional_vocab_if_needed": True,
                    "additional_vocab_must_respect_tolerance": True,
                    "no_grammar_above_base_level": True,
                    "short_instructions": True,
                    "no_extra_keys": True,
                    "no_missing_keys": True
                },
                "exercise_schema": {
                    "mode": "exercise",
                    "exerciseNumber": "integer",
                    "exerciseType": "string",
                    "tasks": [
                        {
                            "type": "string",
                            "instruction": "string"
                        }
                    ]
                }
            }
        },
        "exercise_types": [
            "new_word_drill",
            "repetition_drill",
            "context_usage",
            "mixed_tense_drill",
            "review_self_test"
        ],
        "answer_format": {
            "numbering_optional": True,
            "evaluate_sequentially": True,
            "ignore_numbering_markers": True
        },
        "feedback_mode": {
            "json_only": False,
            "plain_text_only": True,

            "correction_style": "natural_teacher",
            "structured_but_not_robotic": True,
            "group_by_exercise": True,
            "correct_each_task": True,

            "correction_flow": [
                "state_if_correct",
                "provide_correct_version_if_needed",
                "brief_natural_explanation",
                "optional_micro_example_if_helpful"
            ],

            "tone_rules": {
                "avoid_robotic_numbering_inside_explanations": True,
                "avoid_repeating_rule_labels": True,
                "sound_like_human_teacher": True,
                "avoid_unnecessary_theory": True,
                "max_sentences_per_error": 4
            },

            "respect_practice_level": True,
            "include_level_label": True,

            "recommendation_required": True,
            "recommendation_must_match_exact_option": True,
            "recommendation_no_extra_text": True,

            "recommendation_options": [
                "A – Next Exercise",
                "B – Repeat Exercise",
                "C – Micro Drill"
            ],

            "recommendation_logic": {
                "if_multiple_grammar_errors": "C – Micro Drill",
                "if_minor_errors": "B – Repeat Exercise",
                "if_all_correct": "A – Next Exercise"
            }
        },
        "micro_drill": {
            "json_only": True,
            "task_min": 3,
            "task_max": 5,
            "fix_only_detected_issue": True,
            "no_new_complex_vocab": True,
            "no_grammar_above_base_level": True,
            "schema": {
                "mode": "micro_drill",
                "focus": "string",
                "tasks": [
                    {
                        "type": "string",
                        "instruction": "string"
                    }
                ]
            }
        },
        "summary_commands": {
            "show_introduced": {
                "json_only": True,
                "schema": [
                    "string"
                ]
            },
            "show_learned": {
                "json_only": True,
                "schema": [
                    "string"
                ]
            },
            "show_status": {
                "plain_text_only": True
            }
        },
        "general_rules": {
            "never_mix_json_and_text": True,
            "never_change_schema": True,
            "never_add_extra_keys": True,
            "never_remove_keys": True,
            "respect_practice_level": True,
            "do_not_skip_exercise_numbers": True,
            "avoid_internal_repetition": True,
            "user_decides_module_end": True
        }
    }
}

MODULE_2_PLAN = {}
MODULE_3_PLAN = {}
MODULE_4_PLAN = {}
MODULE_5_PLAN = {}