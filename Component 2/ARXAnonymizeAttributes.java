package org.deidentifier.arx.examples;

/*
 * ARX: Powerful Data Anonymization
 * Copyright 2012 - 2021 Fabian Prasser and contributors
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

import org.deidentifier.arx.*;
import org.deidentifier.arx.criteria.KAnonymity;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.concurrent.TimeUnit;
import java.util.stream.Stream;

/**
 * This class implements an example on how to use the API by providing CSV files
 * as input.
 *
 * @author Fabian Prasser
 * @author Florian Kohlmayer
 * MODIFIED by Ryan Hildebrant
 */
public class ARXAnonymizeAttributes extends Example {

    /**
     * Entry point.
     *
     * @param args the arguments
     * @throws IOException
     */
    public static void main(String[] args) throws IOException {
        long count;
        int k = 20;
        try (Stream<Path> files = Files.list(Paths.get("Path\\Vectorization\\k = " + k))) {
            count = files.count();
        }
        long start1 = System.nanoTime();
        for (long file = 1; file < count; file++) {
            try {
                Data data = Data.create("Path\\\Log\\Vectorization\\k = " + k + "\\output_" + file + ".csv", StandardCharsets.UTF_8, ',');

                int columns = data.getHandle().getNumColumns();

                for (int i = 1; i < columns; i++) {
                    data.getDefinition().setAttributeType("row_" + i, AttributeType.Hierarchy.create("hierarchy", StandardCharsets.UTF_8, ','));
                }
                data.getDefinition().setAttributeType("case", AttributeType.INSENSITIVE_ATTRIBUTE);

                ARXAnonymizer anonymizer = new ARXAnonymizer();

                ARXConfiguration config = ARXConfiguration.create();
                config.addPrivacyModel(new KAnonymity(k));
                config.setSuppressionLimit(1.0);
                // config.setSuppressionLimit(0.02d);
                config.setAlgorithm(ARXConfiguration.AnonymizationAlgorithm.BEST_EFFORT_BOTTOM_UP);
                ARXResult result = anonymizer.anonymize(data, config);
                result.getOutput(false).save("Output_"
                        + file + ".csv", ',');
            }
            catch (IllegalArgumentException ignored) {
                System.out.println(ignored);
            }
        }
        long end1 = System.nanoTime();
        long convert = TimeUnit.SECONDS.convert((end1-start1), TimeUnit.NANOSECONDS);
        System.out.println("Elapsed Time in seconds: "+ convert);
    }
}
