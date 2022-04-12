from src.Patterns import Patterns

patterns = Patterns()

query_credit_score_field = '(~CreditScoreDate.isnull() and CreditScore.isnull()) or ' \
                           '(CreditScore < 350 or CreditScore>850)'
query_credit_score_date_field = f"(~CreditScore.isnull() and CreditScoreDate.isnull()) or " \
                                f"~(~CreditScoreDate.isnull() and CreditScoreDate.str.match('{patterns.date}'))"
