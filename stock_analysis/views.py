from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from dal import autocomplete
from .models import Stock, StockData
from .forms import StockForm
from .utils import scrape_stock_data


def stocks(request):
    if request.method == "POST":
        form = StockForm(request.POST)
        if form.is_valid():
            stock_id = request.POST.get("stock")
            stock = Stock.objects.get(pk=stock_id)
            symbol = stock.symbol
            exchange = stock.exchange

            # Fetch stock data
            stock_response = scrape_stock_data(symbol, exchange)

            # Check for errors
            if "error" in stock_response:
                messages.error(request, stock_response["error"])
                context = {"form": form}
                return render(request, "stock_analysis/stocks.html", context)

            # Save to database
            stock_data, created = StockData.objects.update_or_create(
                stock=stock,
                defaults={
                    "current_price": stock_response.get("current_price"),
                    "price_changed": stock_response.get("price_changed"),
                    "percentage_changed": stock_response.get("percentage_changed"),
                    "previous_close": stock_response.get("previous_close"),
                    "week_52_high": stock_response.get("week_52_high"),
                    "week_52_low": stock_response.get("week_52_low"),
                    "market_cap": stock_response.get("market_cap"),
                    "pe_ratio": stock_response.get("pe_ratio"),
                    "dividend_yield": stock_response.get("dividend_yield"),
                },
            )

            action = "updated" if not created else "created"
            messages.success(
                request, f"Stock data {action} successfully for {stock.name}"
            )

            context = {
                "form": form,
                "stock_data": stock_data,
                "stock": stock,
            }
            return redirect("stock_detail", pk=stock_id)
        else:
            messages.error(request, "Form is not valid.")
            context = {"form": form}
            return render(request, "stock_analysis/stocks.html", context)
    else:
        form = StockForm()
        context = {"form": form}
        return render(request, "stock_analysis/stocks.html", context)


def stock_detail(request, pk):
    """Display detailed information for a specific stock"""
    stock = get_object_or_404(Stock, pk=pk)

    # Try to get existing stock data
    try:
        stock_data = StockData.objects.get(stock=stock)
    except StockData.DoesNotExist:
        stock_data = None

    # Option to refresh data
    if request.method == "POST" and "refresh" in request.POST:
        stock_response = scrape_stock_data(stock.symbol, stock.exchange)

        if "error" in stock_response:
            messages.error(request, stock_response["error"])
        else:
            stock_data, created = StockData.objects.update_or_create(
                stock=stock,
                defaults={
                    "current_price": stock_response.get("current_price"),
                    "price_changed": stock_response.get("price_changed"),
                    "percentage_changed": stock_response.get("percentage_changed"),
                    "previous_close": stock_response.get("previous_close"),
                    "week_52_high": stock_response.get("week_52_high"),
                    "week_52_low": stock_response.get("week_52_low"),
                    "market_cap": stock_response.get("market_cap"),
                    "pe_ratio": stock_response.get("pe_ratio"),
                    "dividend_yield": stock_response.get("dividend_yield"),
                },
            )
            messages.success(request, "Stock data refreshed successfully!")
            return redirect("stock_detail", pk=pk)

    context = {
        "stock": stock,
        "stock_data": stock_data,
    }
    return render(request, "stock_analysis/stock_detail.html", context)


class StockAutoComplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Stock.objects.all()
        if self.q:
            qs = qs.filter(name__istartswith=self.q)
        return qs
