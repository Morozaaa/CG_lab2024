import javax.swing.*;
import javax.swing.event.ChangeEvent;
import javax.swing.event.ChangeListener;
import java.awt.*;

class ColorConverterApp extends JFrame {
    // Поля для RGB
    private JSlider redSlider, greenSlider, blueSlider;
    private JTextField redField, greenField, blueField;

    // Поля для HLS
    private JSlider hueSlider, lightnessSlider, saturationSlider;
    private JTextField hueField, lightnessField, saturationField;

    // Поля для CMYK
    private JSlider cyanSlider, magentaSlider, yellowSlider, blackSlider;
    private JTextField cyanField, magentaField, yellowField, blackField;

    private JPanel colorPanel;

    private boolean isUpdating = false;  // Флаг для предотвращения циклов обновлений

    public ColorConverterApp() {
        setTitle("Color Converter: CMYK - RGB - HLS");
        setSize(600, 600);
        setDefaultCloseOperation(EXIT_ON_CLOSE);
        setLayout(new GridLayout(4, 1));

        // Панель для RGB
        JPanel rgbPanel = new JPanel();
        rgbPanel.setLayout(new GridLayout(3, 3));
        redSlider = createSlider(0, 255, 0);
        greenSlider = createSlider(0, 255, 0);
        blueSlider = createSlider(0, 255, 0);
        redField = createTextField();
        greenField = createTextField();
        blueField = createTextField();

        addToPanel(rgbPanel, "Red", redSlider, redField);
        addToPanel(rgbPanel, "Green", greenSlider, greenField);
        addToPanel(rgbPanel, "Blue", blueSlider, blueField);

        // Панель для HLS
        JPanel hlsPanel = new JPanel();
        hlsPanel.setLayout(new GridLayout(3, 3));
        hueSlider = createSlider(0, 360, 0);
        lightnessSlider = createSlider(0, 100, 0);
        saturationSlider = createSlider(0, 100, 0);
        hueField = createTextField();
        lightnessField = createTextField();
        saturationField = createTextField();

        addToPanel(hlsPanel, "Hue", hueSlider, hueField);
        addToPanel(hlsPanel, "Lightness", lightnessSlider, lightnessField);
        addToPanel(hlsPanel, "Saturation", saturationSlider, saturationField);

        // Панель для CMYK
        JPanel cmykPanel = new JPanel();
        cmykPanel.setLayout(new GridLayout(4, 3));
        cyanSlider = createSlider(0, 100, 0);
        magentaSlider = createSlider(0, 100, 0);
        yellowSlider = createSlider(0, 100, 0);
        blackSlider = createSlider(0, 100, 0);
        cyanField = createTextField();
        magentaField = createTextField();
        yellowField = createTextField();
        blackField = createTextField();

        addToPanel(cmykPanel, "Cyan", cyanSlider, cyanField);
        addToPanel(cmykPanel, "Magenta", magentaSlider, magentaField);
        addToPanel(cmykPanel, "Yellow", yellowSlider, yellowField);
        addToPanel(cmykPanel, "Black", blackSlider, blackField);

        // Панель для показа цвета
        colorPanel = new JPanel();
        colorPanel.setBackground(Color.BLACK);

        // Добавление панелей на форму
        add(rgbPanel);
        add(hlsPanel);
        add(cmykPanel);
        add(colorPanel);

        // Слушатели изменений для RGB
        addRgbListeners();
        // Слушатели изменений для HLS
        addHlsListeners();
        // Слушатели изменений для CMYK
        addCmykListeners();

        JPanel colorChooserPanel = new JPanel();
        JButton chooseColorButton = new JButton("Choose Color");
        colorChooserPanel.add(chooseColorButton);
        add(chooseColorButton);
        chooseColorButton.addActionListener(e -> {
            Color selectedColor = JColorChooser.showDialog(this, "Choose a Color", colorPanel.getBackground());
            if (selectedColor != null) {
                int r = selectedColor.getRed();
                int g = selectedColor.getGreen();
                int b = selectedColor.getBlue();
                // Обновляем все модели
                updateFromRgb(r, g, b);
            }
        });
    }

    // Вспомогательные методы
    private JSlider createSlider(int min, int max, int initial) {
        JSlider slider = new JSlider(min, max, initial);
        slider.setMajorTickSpacing((max - min) / 5);
        slider.setPaintTicks(true);
        return slider;
    }

    private JTextField createTextField() {
        return new JTextField(3);
    }

    private void addToPanel(JPanel panel, String label, JSlider slider, JTextField textField) {
        panel.add(new JLabel(label));
        panel.add(slider);
        panel.add(textField);
    }

    // Флаг для предотвращения зацикливания обновлений
private boolean isUpdating1 = false;

private void addRgbListeners() {
    ChangeListener listener = e -> {
        if (isUpdating1) return;  // Пропускаем, если обновление уже идет
        isUpdating1 = true;  // Устанавливаем флаг обновления

        int r = redSlider.getValue();
        int g = greenSlider.getValue();
        int b = blueSlider.getValue();

        // Обновление текстовых полей
        redField.setText(String.valueOf(r));
        greenField.setText(String.valueOf(g));
        blueField.setText(String.valueOf(b));

        // Пересчет в другие модели
        updateFromRgb(r, g, b);

        isUpdating1 = false;  // Сбрасываем флаг обновления
    };

    redSlider.addChangeListener(listener);
    greenSlider.addChangeListener(listener);
    blueSlider.addChangeListener(listener);

    // Добавляем слушателей для текстовых полей
    addTextFieldListenersForRgb();
}

private void addTextFieldListenersForRgb() {
    redField.addActionListener(e -> updateFromTextField(redField, redSlider));
    greenField.addActionListener(e -> updateFromTextField(greenField, greenSlider));
    blueField.addActionListener(e -> updateFromTextField(blueField, blueSlider));
}

private void addHlsListeners() {
    ChangeListener listener = e -> {
        if (isUpdating1) return;  // Пропускаем, если обновление уже идет
        isUpdating1 = true;  // Устанавливаем флаг обновления

        int h = hueSlider.getValue();
        int l = lightnessSlider.getValue();
        int s = saturationSlider.getValue();

        // Обновление текстовых полей
        hueField.setText(String.valueOf(h));
        lightnessField.setText(String.valueOf(l));
        saturationField.setText(String.valueOf(s));

        // Пересчет в другие модели
        updateFromHls(h, l, s);

        isUpdating1 = false;  // Сбрасываем флаг обновления
    };

    hueSlider.addChangeListener(listener);
    lightnessSlider.addChangeListener(listener);
    saturationSlider.addChangeListener(listener);

    // Добавляем слушателей для текстовых полей
    addTextFieldListenersForHls();
}

private void addTextFieldListenersForHls() {
    hueField.addActionListener(e -> updateFromTextField(hueField, hueSlider));
    lightnessField.addActionListener(e -> updateFromTextField(lightnessField, lightnessSlider));
    saturationField.addActionListener(e -> updateFromTextField(saturationField, saturationSlider));
}

private void addCmykListeners() {
    ChangeListener listener = e -> {
        if (isUpdating1) return;  // Пропускаем, если обновление уже идет
        isUpdating1 = true;  // Устанавливаем флаг обновления

        int c = cyanSlider.getValue();
        int m = magentaSlider.getValue();
        int y = yellowSlider.getValue();
        int k = blackSlider.getValue();

        // Обновление текстовых полей
        cyanField.setText(String.valueOf(c));
        magentaField.setText(String.valueOf(m));
        yellowField.setText(String.valueOf(y));
        blackField.setText(String.valueOf(k));

        // Пересчет в другие модели
        updateFromCmyk(c, m, y, k);

        isUpdating1 = false;  // Сбрасываем флаг обновления
    };

    cyanSlider.addChangeListener(listener);
    magentaSlider.addChangeListener(listener);
    yellowSlider.addChangeListener(listener);
    blackSlider.addChangeListener(listener);

    // Добавляем слушателей для текстовых полей
    addTextFieldListenersForCmyk();
}

private void addTextFieldListenersForCmyk() {
    cyanField.addActionListener(e -> updateFromTextField(cyanField, cyanSlider));
    magentaField.addActionListener(e -> updateFromTextField(magentaField, magentaSlider));
    yellowField.addActionListener(e -> updateFromTextField(yellowField, yellowSlider));
    blackField.addActionListener(e -> updateFromTextField(blackField, blackSlider));
}

private void updateFromTextField(JTextField textField, JSlider slider) {
    try {
        int value = Integer.parseInt(textField.getText());
        if(textField==magentaField || textField==blackField || textField==hueField || textField==yellowField || textField==cyanField || textField==lightnessField || textField==saturationField){
            value*=100;
        }
        if (value >= slider.getMinimum() && value <= slider.getMaximum()) {
            if (!isUpdating) {  // Проверяем, идет ли обновление
                isUpdating = true;  // Устанавливаем флаг
                slider.setValue(value);  // Обновляем слайдер
                isUpdating = false;  // Сбрасываем флаг
            }
        } else {
            textField.setText(String.valueOf(slider.getValue()));  // Восстанавливаем старое значение
        }
    } catch (NumberFormatException ex) {
        textField.setText(String.valueOf(slider.getValue()));  // Восстанавливаем старое значение при ошибке
    }
}


    // Методы пересчета цвета из разных моделей
    private void updateFromRgb(int r, int g, int b) {
        // Преобразование RGB в HSB (HLS аналог)
        float[] hsb = Color.RGBtoHSB(r, g, b, null);
        hueSlider.setValue((int) (hsb[0] * 360));  // Hue в градусах
        saturationSlider.setValue((int) (hsb[1] * 100));  // Saturation в процентах
        lightnessSlider.setValue((int) (hsb[2] * 100));   // Brightness (Lightness) в процентах
    
        hueField.setText(String.format("%.2f", hsb[0]));  // Hue от 0 до 1
        saturationField.setText(String.format("%.2f", hsb[1]));  // Saturation от 0 до 1
        lightnessField.setText(String.format("%.2f", hsb[2]));  // Lightness от 0 до 1
    
        // Преобразование RGB в CMYK
        float[] cmyk = rgbToCmyk(r, g, b);
        cyanSlider.setValue((int) (cmyk[0] * 100));
        magentaSlider.setValue((int) (cmyk[1] * 100));
        yellowSlider.setValue((int) (cmyk[2] * 100));
        blackSlider.setValue((int) (cmyk[3] * 100));
    
        cyanField.setText(String.format("%.2f", cmyk[0]));  // Cyan от 0 до 1
        magentaField.setText(String.format("%.2f", cmyk[1]));  // Magenta от 0 до 1
        yellowField.setText(String.format("%.2f", cmyk[2]));  // Yellow от 0 до 1
        blackField.setText(String.format("%.2f", cmyk[3]));  // Black от 0 до 1
    
        // Обновляем цвет панели
        Color color = new Color(r, g, b);
        colorPanel.setBackground(color);
    }
    
    private void updateFromHls(int h, int l, int s) {
        // Преобразование HLS в RGB (используем HSB в Java)
        float hue = h / 360.0f;
        float saturation = s / 100.0f;
        float lightness = l / 100.0f;
    
        int rgb = Color.HSBtoRGB(hue, saturation, lightness);
        int r = (rgb >> 16) & 0xFF;
        int g = (rgb >> 8) & 0xFF;
        int b = rgb & 0xFF;
    
        redSlider.setValue(r);
        greenSlider.setValue(g);
        blueSlider.setValue(b);
    
        redField.setText(String.valueOf(r));
        greenField.setText(String.valueOf(g));
        blueField.setText(String.valueOf(b));
    
        hueField.setText(String.format("%.2f", hue));  // Hue от 0 до 1
        saturationField.setText(String.format("%.2f", saturation));  // Saturation от 0 до 1
        lightnessField.setText(String.format("%.2f", lightness));  // Lightness от 0 до 1
    
        // Пересчет в CMYK
        updateFromRgb(r, g, b);
    }
    
    private void updateFromCmyk(int c, int m, int y, int k) {
        // Преобразование CMYK в RGB
        int[] rgb = cmykToRgb(c / 100.0f, m / 100.0f, y / 100.0f, k / 100.0f);
        redSlider.setValue(rgb[0]);
        greenSlider.setValue(rgb[1]);
        blueSlider.setValue(rgb[2]);
    
        redField.setText(String.valueOf(rgb[0]));
        greenField.setText(String.valueOf(rgb[1]));
        blueField.setText(String.valueOf(rgb[2]));
    
        cyanField.setText(String.format("%.2f", c / 100.0f));  // Cyan от 0 до 1
        magentaField.setText(String.format("%.2f", m / 100.0f));  // Magenta от 0 до 1
        yellowField.setText(String.format("%.2f", y / 100.0f));  // Yellow от 0 до 1
        blackField.setText(String.format("%.2f", k / 100.0f));  // Black от 0 до 1
    
        // Пересчет в HLS
        updateFromRgb(rgb[0], rgb[1], rgb[2]);
    }
    
    

    // Методы преобразования
    private float[] rgbToHls(int r, int g, int b) {
        float[] hls = new float[3];
        Color.RGBtoHSB(r, g, b, hls);
        hls[0] = hls[0] * 360;  // Hue в градусах
        hls[1] = hls[1];        // Saturation
        hls[2] = hls[2];        // Lightness
        return hls;
    }

    private int[] hlsToRgb(float h, float l, float s) {
        int rgb = Color.HSBtoRGB(h / 360.0f, s, l);
        return new int[] { (rgb >> 16) & 0xFF, (rgb >> 8) & 0xFF, rgb & 0xFF };
    }

    private float[] rgbToCmyk(int r, int g, int b) {
        float c = 1 - (r / 255.0f);
        float m = 1 - (g / 255.0f);
        float y = 1 - (b / 255.0f);

        float k = Math.min(c, Math.min(m, y));

        if (k < 1) {
            c = (c - k) / (1 - k);
            m = (m - k) / (1 - k);
            y = (y - k) / (1 - k);
        } else {
            c = 0;
            m = 0;
            y = 0;
        }

        return new float[] {c, m, y, k};
    }

    private int[] cmykToRgb(float c, float m, float y, float k) {
        int r = (int) ((1 - c) * (1 - k) * 255);
        int g = (int) ((1 - m) * (1 - k) * 255);
        int b = (int) ((1 - y) * (1 - k) * 255);
        return new int[] {r, g, b};
    }

    public static void main(String[] args) {
        SwingUtilities.invokeLater(() -> {
            new ColorConverterApp().setVisible(true);
        });
    }
}
