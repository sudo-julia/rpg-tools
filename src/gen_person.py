# take user input to help generate a person
# i wrote this in a few minutes so apologies for code quality

# TODO make more info optional as args
# TODO home station/planet generator

import argparse
from random import choice, randint
from faker import Faker
from nonbinary_provider import Provider as NonbinaryProvider
from lib.to_output import to_output


# TODO find other formatting for better looking output to GUI (remove returns?)
def format_person(name: str, company: str, job: str, age: int, gender: str):
    """print the person generated by gen_person"""
    person = f"""
        \r{name}
        \r{'-' * len(name)}
        \r- Age: {age}
        \r- Gender: {gender.title()}
        \r- Company: {company}
        \r- Job: {job}\n""".lstrip()
    return person


def gen_person(gender: str, age_group: str):
    """generate a person and gather some additional info"""
    if gender == "female":
        name = fake.name_female()
    elif gender == "male":
        name = fake.name_male()
    else:
        gender = "nonbinary"
        # 25% chance to skip the last name (it usually sounds really cool)
        if randint(1, 4) > 3:
            name = fake.real_name_nonbinary()
        else:
            name = f"{fake.real_name_nonbinary()} {fake.last_name()}"

    name = give_prefix(name, gender)
    name = give_suffix(name, gender)
    company = fake.company()
    job = fake.job()

    age = give_age(age_group)
    return name, company, job, age


def give_age(age_group: str):
    """give an npc an age"""
    # age ranges for pilot licenses
    if age_group == "young":
        return randint(20, 35)
    elif age_group == "middle":
        return randint(36, 50)
    elif age_group == "old":
        return randint(51, 60)
    else:
        return None


# TODO is there a way to shorten this to one call?
#      fake.prefix_{gender} + ' ' + name
def give_prefix(name: str, gender: str):
    """12.5% chance to assign a prefix to a name"""
    prefix_chance = randint(1, 8)
    if prefix_chance > 7:
        if gender == "female":
            name = f"{fake.prefix_female()} {name}"
        elif gender == "male":
            name = f"{fake.prefix_male()} {name}"
        else:
            name = f"{fake.prefix_nonbinary()} {name}"
    return name


def give_suffix(name: str, gender: str):
    """12.5% chance to assign a suffix to a name"""
    suffix_chance = randint(1, 8)
    if suffix_chance > 7:
        if gender == "female":
            name = f"{name} {fake.suffix_female()}"
        elif gender == "male":
            name = f"{name} {fake.suffix_male()}"
        else:
            name = f"{name} {fake.suffix_nonbinary()}"
    return name


def parse_arguments():
    """sort through provided arguments to set variables"""
    parser = argparse.ArgumentParser()

    # group for age ranges to pass to functions
    age_group = parser.add_mutually_exclusive_group()
    age_group.add_argument("--young", help="create a younger npc", action="store_true")
    age_group.add_argument(
        "--middle", help="create a middle-aged npc", action="store_true"
    )
    age_group.add_argument("--old", help="create an old npc", action="store_true")

    # cannot select more than one gender (not irl, just for name)
    gender_group = parser.add_mutually_exclusive_group(required=False)
    gender_group.add_argument(
        "-f",
        "--female",
        help="generate a Female npc",
        action="store_true",
    )
    gender_group.add_argument(
        "-n", "--nonbinary", help="generate a Nonbinary npc", action="store_true"
    )
    gender_group.add_argument(
        "-m", "--male", help="generate a male npc", action="store_true"
    )
    gender_group.add_argument(
        "-r",
        "--random",
        help="create a randomized npc (default)",
        action="store_true",
    )

    parser.add_argument(
        "-o",
        "--output",
        help="""write to stdout and file. defaults to
        location specified in config""",
        action="store_true",
    )

    args = parser.parse_args()

    # if random is given, ignore all other flags and generate npc with random params
    if args.random:
        pass

    # since age_group is optional during generation, a None value won't break the func
    if args.young:
        age_group = "young"
    elif args.middle:
        age_group = "middle"
    elif args.old:
        age_group = "old"
    else:
        age_group = choice(["young", "middle", "old"])

    if args.female:
        gender = "female"
    elif args.nonbinary:
        if randint(1, 10) > 1:
            gender = "nonbinary"
        else:
            gender = "None"
    elif args.male:
        gender = "male"
    else:
        gender = choice(["female", "nonbinary", "male"])

    if args.output:
        output = True
    else:
        output = None

    name, company, job, age = gen_person(gender, age_group)
    return name, company, job, age, gender, output


def main():
    """generate an npc with provided gender"""
    name, company, job, age, gender, output = parse_arguments()
    person = format_person(name, company, job, age, gender)
    print(person)
    if output:
        to_output("GenPerson", f"{person}\n")
    exit(0)


fake = Faker("en_us")
fake.add_provider(NonbinaryProvider)

if __name__ == "__main__":
    main()
