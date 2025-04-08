# score_calculator.py

def calculate_age_score(age, has_partner):
    """
    根据用户的年龄计算年龄得分。
    :param age: int, 用户年龄
    :param has_partner: str, 是否有配偶 ("yes" 或 "no")
    :return: int, 年龄得分
    """
    if has_partner == 'yes':
        if 18 <= age <= 29:
            return 100
        elif 30 <= age <= 39:
            return 95
        elif 40 <= age <= 45:
            return 50
        else:
            return 0  # 超过45岁或小于18岁，得分为0
    else:
        if 18 <= age <= 29:
            return 110
        elif 30 <= age <= 39:
            return 105
        elif 40 <= age <= 45:
            return 60
        else:
            return 0

def calculate_education_score(education_level, has_partner):
    """
    根据用户的教育水平计算得分。
    :param education_level: str, 教育水平代码
    :param has_partner: str, 是否有配偶 ("yes" 或 "no")
    :return: int, 教育水平得分
    """
    education_scores_with_partner = {
        "less_than_secondary": 0,
        "secondary_diploma": 28,
        "one_year_degree": 84,
        "two_year_program": 91,
        "bachelor_degree": 112,
        "two_or_more_degrees": 119,
        "masters_or_professional": 126,
        "doctoral_degree": 140
    }

    education_scores_without_partner = {
        "less_than_secondary": 0,
        "secondary_diploma": 30,
        "one_year_degree": 90,
        "two_year_program": 98,
        "bachelor_degree": 120,
        "two_or_more_degrees": 128,
        "masters_or_professional": 135,
        "doctoral_degree": 150
    }

    if has_partner == 'yes':
        return education_scores_with_partner.get(education_level, 0)
    else:
        return education_scores_without_partner.get(education_level, 0)

def calculate_english_score(reading, writing, speaking, listening, has_partner):
    """
    根据用户的英语能力 (阅读、写作、口语、听力) 计算得分。
    :param reading: str, 阅读能力等级
    :param writing: str, 写作能力等级
    :param speaking: str, 口语能力等级
    :param listening: str, 听力能力等级
    :param has_partner: str, 是否有配偶 ("yes" 或 "no")
    :return: int, 英语能力总得分
    """
    english_scores = {
        "less_than_clb4": 0,
        "clb_4_or_5": 6 if has_partner == 'yes' else 6,
        "clb_6": 8 if has_partner == 'yes' else 9,
        "clb_7": 16 if has_partner == 'yes' else 17,
        "clb_8": 22 if has_partner == 'yes' else 23,
        "clb_9": 29 if has_partner == 'yes' else 31,
        "clb_10_or_more": 32 if has_partner == 'yes' else 34
    }

    total_score = (
        english_scores.get(reading, 0) +
        english_scores.get(writing, 0) +
        english_scores.get(speaking, 0) +
        english_scores.get(listening, 0)
    )
    
    return total_score

def calculate_french_score(reading, writing, speaking, listening, has_partner):
    """
    根据用户的法语能力 (阅读、写作、口语、听力) 计算得分。
    :param reading: str, 阅读能力等级
    :param writing: str, 写作能力等级
    :param speaking: str, 口语能力等级
    :param listening: str, 听力能力等级
    :param has_partner: str, 是否有配偶 ("yes" 或 "no")
    :return: int, 法语能力总得分
    """
    french_scores = {
        "less_than_clb4": 0,
        "clb_5_or_6": 1 if has_partner == 'yes' else 1,
        "clb_7_or_8": 3 if has_partner == 'yes' else 3,
        "clb_9_or_more": 6 if has_partner == 'yes' else 6
    }

    total_score = (
        french_scores.get(reading, 0) +
        french_scores.get(writing, 0) +
        french_scores.get(speaking, 0) +
        french_scores.get(listening, 0)
    )

    return total_score

def calculate_canadian_experience_score(years_of_experience, has_partner):
    """
    根据用户在加拿大的工作年限计算得分。
    :param years_of_experience: str, 工作年限代码
    :param has_partner: str, 是否有配偶 ("yes" 或 "no")
    :return: int, 加拿大工作经验得分
    """
    experience_scores = {
        "none_or_less_than_one": 0,
        "one_year": 35 if has_partner == 'yes' else 40,
        "two_years": 46 if has_partner == 'yes' else 53,
        "three_years": 56 if has_partner == 'yes' else 64,
        "four_years": 63 if has_partner == 'yes' else 72,
        "five_or_more_years": 70 if has_partner == 'yes' else 80
    }

    return experience_scores.get(years_of_experience, 0)

def calculate_core_human_capital_score(age, has_partner, education_level, english_reading, english_writing, english_speaking, english_listening, french_reading, french_writing, french_speaking, french_listening, years_of_experience):
    """
    计算核心人力资本因素的总得分。
    :param age: int, 年龄
    :param has_partner: str, 是否有配偶 ("yes" 或 "no")
    :param education_level: str, 教育水平代码
    :param english_reading: str, 英语阅读能力等级
    :param english_writing: str, 英语写作能力等级
    :param english_speaking: str, 英语口语能力等级
    :param english_listening: str, 英语听力能力等级
    :param french_reading: str, 法语阅读能力等级
    :param french_writing: str, 法语写作能力等级
    :param french_speaking: str, 法语口语能力等级
    :param french_listening: str, 法语听力能力等级
    :param years_of_experience: str, 加拿大工作年限代码
    :return: int, 核心人力资本总分
    """
    # 计算每个因素的分数
    age_score = calculate_age_score(age, has_partner)
    education_score = calculate_education_score(education_level, has_partner)
    english_score = calculate_english_score(english_reading, english_writing, english_speaking, english_listening, has_partner)
    french_score = calculate_french_score(french_reading, french_writing, french_speaking, french_listening, has_partner)
    language_score = english_score + french_score
    canadian_experience_score = calculate_canadian_experience_score(years_of_experience, has_partner)
    
    # 核心人力资本总分
    total_score = age_score + education_score + language_score + canadian_experience_score
    return total_score



def calculate_spouse_education_score(spouse_education_level):
    """
    计算配偶的教育水平得分。
    :param spouse_education_level: str, 配偶的教育水平代码
    :return: int, 教育水平得分
    """
    spouse_education_scores = {
        "less_than_secondary": 0,
        "secondary_diploma": 2,
        "one_year_degree": 6,
        "two_year_program": 7,
        "bachelor_degree": 8,
        "two_or_more_degrees": 9,
        "masters_or_professional": 10,
        "doctoral_degree": 10
    }
    return spouse_education_scores.get(spouse_education_level, 0)

def calculate_spouse_language_score(reading, writing, speaking, listening):
    """
    计算配偶的语言能力得分。
    :param reading: str, 阅读能力等级
    :param writing: str, 写作能力等级
    :param speaking: str, 口语能力等级
    :param listening: str, 听力能力等级
    :return: int, 语言能力得分
    """
    spouse_language_scores = {
        "less_than_clb4": 0,
        "clb_5_or_6": 1,
        "clb_7_or_8": 3,
        "clb_9_or_more": 5
    }
    
    total_language_score = (
        spouse_language_scores.get(reading, 0) +
        spouse_language_scores.get(writing, 0) +
        spouse_language_scores.get(speaking, 0) +
        spouse_language_scores.get(listening, 0)
    )

    # 限制语言得分最高为 20 分
    return min(total_language_score, 20)

def calculate_spouse_experience_score(spouse_years_of_experience):
    """
    计算配偶的工作经验得分。
    :param spouse_years_of_experience: str, 配偶的工作年限代码
    :return: int, 工作经验得分
    """
    spouse_experience_scores = {
        "none_or_less_than_one": 0,
        "one_year": 5,
        "two_years": 7,
        "three_years": 8,
        "four_years": 9,
        "five_or_more_years": 10
    }
    return spouse_experience_scores.get(spouse_years_of_experience, 0)

def calculate_spouse_score(spouse_education_level, spouse_english_reading, spouse_english_writing, spouse_english_speaking, spouse_english_listening, spouse_years_of_experience):
    """
    根据配偶或同居伴侣的教育水平、语言能力和工作经验计算得分。
    :param spouse_education_level: str, 配偶的教育水平代码
    :param spouse_english_reading: str, 配偶的英语阅读能力等级
    :param spouse_english_writing: str, 配偶的英语写作能力等级
    :param spouse_english_speaking: str, 配偶的英语口语能力等级
    :param spouse_english_listening: str, 配偶的英语听力能力等级
    :param spouse_years_of_experience: str, 配偶的工作年限代码
    :return: dict, 包含各个评分项和总得分的字典
    """
    # 分别计算配偶的各个得分
    education_score = calculate_spouse_education_score(spouse_education_level)
    language_score = calculate_spouse_language_score(spouse_english_reading, spouse_english_writing, spouse_english_speaking, spouse_english_listening)
    experience_score = calculate_spouse_experience_score(spouse_years_of_experience)

    # 计算总得分
    total_score = education_score + language_score + experience_score

    return {
        "education_score": education_score,
        "language_score": language_score,
        "experience_score": experience_score,
        "total_score": total_score
    }



def calculate_education_language_skill_transferability_score(education_level, first_language_scores):
    """
    计算基于教育和官方语言能力结合的技能迁移因素得分。
    :param education_level: str, 教育水平代码
    :param first_language_scores: dict, 第一官方语言各项能力的等级，键为 'reading', 'writing', 'speaking', 'listening'
    :return: int, 技能迁移因素得分
    """
    # 定义教育水平对应的分数
    # 注意：根据您提供的评分标准，需要确保 education_level 的取值与评分标准匹配
    score_table = {
        "less_than_secondary": { "clb_7_or_more": 0, "clb_9_or_more": 0 },
        "secondary_diploma":    { "clb_7_or_more": 0, "clb_9_or_more": 0 },
        "one_year_degree":      { "clb_7_or_more": 13, "clb_9_or_more": 25 },
        "two_or_more_degrees":  { "clb_7_or_more": 25, "clb_9_or_more": 50 },
        "bachelor_degree":      { "clb_7_or_more": 25, "clb_9_or_more": 50 },
        "masters_or_professional": { "clb_7_or_more": 25, "clb_9_or_more": 50 },
        "doctoral_degree":      { "clb_7_or_more": 25, "clb_9_or_more": 50 }
    }

    # 获取用户的教育水平得分配置
    education_scores = score_table.get(education_level, {"clb_7_or_more": 0, "clb_9_or_more": 0})

    # 检查第一官方语言各项能力是否达到 CLB 7 及以上
    all_clb7_or_higher = all(
        score in ["clb_7", "clb_8", "clb_9", "clb_10_or_more"] for score in first_language_scores.values()
    )

    # 检查第一官方语言各项能力是否达到 CLB 9 及以上
    all_clb9_or_higher = all(
        score in ["clb_9", "clb_10_or_more"] for score in first_language_scores.values()
    )

    # 根据语言能力等级，选择对应的得分
    if all_clb9_or_higher:
        score = education_scores["clb_9_or_more"]
    elif all_clb7_or_higher:
        score = education_scores["clb_7_or_more"]
    else:
        score = 0

    return score

def calculate_education_canadian_experience_skill_transferability_score(education_level, canadian_experience):
   
    """
    计算基于教育和加拿大工作经验结合的技能迁移因素得分。
    :param education_level: str, 教育水平代码
    :param canadian_experience: str, 加拿大工作经验代码
    :return: int, 技能迁移因素得分
    """

    # 定义教育水平对应的分数
    score_table = {
        "less_than_secondary": {"1_year": 0, "2_or_more_years": 0},
        "secondary_diploma": {"1_year": 0, "2_or_more_years": 0},
        "one_year_degree": {"1_year": 13, "2_or_more_years": 25},
        "two_year_program": {"1_year": 13, "2_or_more_years": 25},
        "bachelor_degree": {"1_year": 25, "2_or_more_years": 50},
        "two_or_more_degrees": {"1_year": 25, "2_or_more_years": 50},
        "masters_or_professional": {"1_year": 25, "2_or_more_years": 50},
        "doctoral_degree": {"1_year": 25, "2_or_more_years": 50}
    }

    # 将加拿大工作经验映射到相应的类别
    if canadian_experience in ["two_years", "three_years", "four_years", "five_or_more_years"]:
        experience_category = "2_or_more_years"
    elif canadian_experience == "one_year":
        experience_category = "1_year"
    else:
        experience_category = "no_experience"

    if experience_category == "no_experience":
        return 0
    else:
        education_scores = score_table.get(education_level, {"1_year": 0, "2_or_more_years": 0})
        score = education_scores.get(experience_category, 0)
        return score
    



def calculate_foreign_canadian_experience_skill_transferability_score(foreign_work_experience, canadian_experience):
    """
    计算基于海外工作经验和加拿大工作经验结合的技能迁移因素得分。
    :param foreign_work_experience: str, 海外工作经验代码
    :param canadian_experience: str, 加拿大工作经验代码
    :return: int, 技能迁移因素得分
    """
    # 定义得分表
    score_table = {
        "no_foreign_experience": {"1_year": 0, "2_or_more_years": 0},
        "one_or_two_years": {"1_year": 13, "2_or_more_years": 25},
        "three_or_more_years": {"1_year": 25, "2_or_more_years": 50}
    }

    # 将加拿大工作经验映射到相应的类别
    if canadian_experience in ["two_years", "three_years", "four_years", "five_or_more_years"]:
        canadian_experience_category = "2_or_more_years"
    elif canadian_experience == "one_year":
        canadian_experience_category = "1_year"
    else:
        canadian_experience_category = "no_canadian_experience"

    if canadian_experience_category == "no_canadian_experience":
        return 0
    else:
        foreign_experience_scores = score_table.get(foreign_work_experience, {"1_year": 0, "2_or_more_years": 0})
        score = foreign_experience_scores.get(canadian_experience_category, 0)
        return score





def calculate_foreign_work_experience_language_skill_transferability_score(foreign_work_experience, first_language_scores):
    """
    计算基于海外工作经验和官方语言能力结合的技能迁移因素得分。
    :param foreign_work_experience: str, 海外工作经验代码
    :param first_language_scores: dict, 第一官方语言各项能力的等级，键为 'reading', 'writing', 'speaking', 'listening'
    :return: int, 技能迁移因素得分
    """
    # 定义得分表
    score_table = {
        "no_foreign_experience": {"clb_7_or_more": 0, "clb_9_or_more": 0},
        "one_or_two_years": {"clb_7_or_more": 13, "clb_9_or_more": 25},
        "three_or_more_years": {"clb_7_or_more": 25, "clb_9_or_more": 50}
    }

    # 检查第一官方语言各项能力是否达到 CLB 7 及以上
    all_clb7_or_higher = all(
        score in ["clb_7", "clb_8", "clb_9", "clb_10_or_more"] for score in first_language_scores.values()
    )

    # 检查第一官方语言各项能力是否达到 CLB 9 及以上
    all_clb9_or_higher = all(
        score in ["clb_9", "clb_10_or_more"] for score in first_language_scores.values()
    )

    if all_clb9_or_higher:
        language_level = "clb_9_or_more"
    elif all_clb7_or_higher:
        language_level = "clb_7_or_more"
    else:
        language_level = "below_clb_7"

    if language_level == "below_clb_7":
        return 0
    else:
        foreign_experience_scores = score_table.get(foreign_work_experience, {"clb_7_or_more": 0, "clb_9_or_more": 0})
        score = foreign_experience_scores.get(language_level, 0)
        return score
    


def calculate_certificate_skill_transferability_score(has_certificate, first_language_scores):
    """
    计算技能迁移因素 - 证书维度的得分。
    :param has_certificate: str, 是否拥有加拿大职业资格证书，取值为 "yes" 或 "no"
    :param first_language_scores: dict, 第一官方语言各项能力的等级，键为 'reading', 'writing', 'speaking', 'listening'
    :return: int, 技能迁移因素 - 证书维度的得分
    """
    if has_certificate != 'yes':
        return 0  # 没有资格证书，得分为 0

    # 检查第一官方语言各项能力是否达到 CLB 5 及以上
    all_clb5_or_higher = all(
        score in ["clb_5", "clb_6", "clb_7", "clb_8", "clb_9", "clb_10_or_more"] for score in first_language_scores.values()
    )

    if not all_clb5_or_higher:
        return 0  # 任意一项低于 CLB 5，得分为 0

    # 检查第一官方语言各项能力是否达到 CLB 7 及以上
    all_clb7_or_higher = all(
        score in ["clb_7", "clb_8", "clb_9", "clb_10_or_more"] for score in first_language_scores.values()
    )

    if all_clb7_or_higher:
        return 50  # 四项能力均达到 CLB 7 或以上，得分为 50
    else:
        return 25  # 至少一项在 CLB 5 或 CLB 6，得分为 25
    


def calculate_canadian_education_points(education_level):
    """
    计算加拿大教育背景的额外加分。
    :param education_level: str, 用户在加拿大获得的教育水平
    :return: int, 加分
    """
    if education_level in ['one_year_degree', 'two_year_program']:
        return 15  # 一至两年的加拿大高等教育学历证书
    elif education_level in ['bachelor_degree', 'two_or_more_degrees', 'masters_or_professional', 'doctoral_degree']:
        return 30  # 三年或以上的加拿大高等教育学历证书
    else:
        return 0  # 不符合加分条件
    
def calculate_sibling_in_canada_points(sibling_in_canada):
    """
    计算在加拿大有兄弟姐妹的额外加分。
    :param sibling_in_canada: str, 'yes' 或 'no'
    :return: int, 加分
    """
    if sibling_in_canada == 'yes':
        return 15
    else:
        return 0
    

def calculate_french_language_additional_points(french_scores, english_scores):
    """
    计算法语语言能力的额外加分。
    :param french_scores: dict, 法语能力，键为 'reading', 'writing', 'speaking', 'listening'
    :param english_scores: dict, 英语能力，键为 'reading', 'writing', 'speaking', 'listening'
    :return: int, 加分
    """
    # 映射法语成绩到 CLB 等级
    french_clb_mapping = {
        'less_than_clb4': 3,
        'clb_5_or_6': 5,
        'clb_7_or_8': 7,
        'clb_9_or_more': 9
    }

    # 映射英语成绩到 CLB 等级
    english_clb_mapping = {
        'less_than_clb4': 3,
        'clb_4_or_5': 4,
        'clb_6': 6,
        'clb_7': 7,
        'clb_8': 8,
        'clb_9': 9,
        'clb_10_or_more': 10
    }

    # 转换法语成绩
    french_clb_scores = [french_clb_mapping.get(score, 0) for score in french_scores.values()]
    # 转换英语成绩
    english_clb_scores = [english_clb_mapping.get(score, 0) for score in english_scores.values()]

    # 检查法语四项是否均达到 NCLC 7 或以上
    french_nclc7_or_higher = all(score >= 7 for score in french_clb_scores)

    if not french_nclc7_or_higher:
        return 0  # 不符合条件，无加分

    # 检查英语四项是否均为 CLB 4 或以下
    english_clb4_or_lower = all(score <= 4 for score in english_clb_scores)
    # 检查英语四项是否均为 CLB 5 或以上
    english_clb5_or_higher = all(score >= 5 for score in english_clb_scores)

    if english_clb4_or_lower:
        return 25
    elif english_clb5_or_higher:
        return 50
    else:
        return 0  # 不符合条件，无加分

def calculate_arranged_employment_points(arranged_employment):
    """
    计算安排好的工作的额外加分。
    :param arranged_employment: str, 'none', 'teer_0_major_00', 'teer_1_2_3_or_other_0'
    :return: int, 加分
    """
    if arranged_employment == 'teer_0_major_00':
        return 200
    elif arranged_employment == 'teer_1_2_3_or_other_0':
        return 50
    else:
        return 0

def calculate_provincial_nomination_points(provincial_nomination):
    """
    计算省提名的额外加分。
    :param provincial_nomination: str, 'yes' 或 'no'
    :return: int, 加分
    """
    if provincial_nomination == 'yes':
        return 600
    else:
        return 0   


