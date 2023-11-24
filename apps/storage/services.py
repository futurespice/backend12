from apps.accounts.models import CustomUser, EmployeeSchedule

from .models import (
    AvailableAtTheBranch,
    Category,
    Ingredient,
    Item,
    ReadyMadeProduct,
)


def get_employees():
    """Get all employees except clients"""
    employees = CustomUser.objects.exclude(position="client").filter(is_active=True)
    return employees


def get_specific_employee(pk):
    """Get specific employee"""
    employee = CustomUser.objects.filter(pk=pk).first()
    return employee


def get_specific_category(pk):
    """Get specific category"""
    category = Category.objects.filter(pk=pk).first()
    return category


def get_categories():
    """Get all categories"""
    categories = Category.objects.all()
    return categories


def get_ingrediants():
    """Get all ingrediants"""
    ingrediants = Ingredient.objects.all()
    return ingrediants


def get_available_at_the_branch():
    """Get all available at the branch"""
    available_at_the_branch = AvailableAtTheBranch.objects.all()
    return available_at_the_branch


def get_items():
    """Get all items"""
    items = Item.objects.all()
    return items


def get_ready_made_products():
    """Get all ready made products"""
    ready_made_products = ReadyMadeProduct.objects.all()
    return ready_made_products


def delete_employee_schedule_by_employee(employee):
    """Delete employee schedule by employee"""
    title = f"{employee.first_name}'s schedule"
    try:
        employee_schedule = EmployeeSchedule.objects.filter(title=title).first()
        employee_schedule.delete()
        return employee_schedule
    except AttributeError:
        return None
